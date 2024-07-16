import os
import openai
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.enum.text import PP_PARAGRAPH_ALIGNMENT
from pptx.dml.color import RGBColor
import time
from dotenv import load_dotenv
from bing_image_downloader import downloader
import certifi

load_dotenv()

# Set the SSL certificate file environment variable
os.environ['SSL_CERT_FILE'] = certifi.where()

# Set up your OpenAI API key
openai.api_key = os.getenv('OPENAI_API_KEY')
buyer_name = "American Water"
buyer_industry = "Water Utility"  # Add the buyer's industry
open_ai_assistant_name = 'Presentation Generator'
last_message_timestamp = 0


def get_assistant_id_by_name(client, assistant_name):
    list_assistants = client.beta.assistants.list()
    for assistant in list_assistants:
        if assistant.name == assistant_name:
            return assistant.id
    raise Exception(f"No Assistant with name '{assistant_name}' found on OpenAI!")


def start_new_conversation(client):
    new_thread = client.beta.threads.create()
    return new_thread


def send_message(client, conversation, assistant_id, content):
    print(f"Sending message to assistant:\n{content}")
    client.beta.threads.messages.create(
        thread_id=conversation.id,
        role="user",
        content=content
    )
    client.beta.threads.runs.create_and_poll(
        thread_id=conversation.id,
        assistant_id=assistant_id
    )


def has_message_completed(message):
    if 'content' not in message.dict():
        return False
    if len(message.dict()['content']) < 1:
        return False
    if 'text' not in message.dict()['content'][0]:
        return False
    if 'value' not in message.dict()['content'][0]['text']:
        return False
    return True


def get_assistant_response(client, conversation, last_message_timestamp):
    try:
        messages = client.beta.threads.messages.list(thread_id=conversation.id, limit=20)
        if messages is None:
            return None

        for message in messages:
            if message.role == 'assistant' and has_message_completed(message):
                if message.created_at > last_message_timestamp:
                    last_message_timestamp = message.created_at
                    return message
        return None
    except Exception as e:
        print(f"Unable to retrieve assistant response: {e}")
        return None


# Function to upload images and get a summary from the assistant
def get_summary_from_assistant(client, assistant_name, images_folder, buyer_name):
    assistant_id = get_assistant_id_by_name(client, assistant_name)
    conversation = start_new_conversation(client)

    # Prepare the content to send
    content = f"Buyer's name: {buyer_name}\nImages:\n"
    for filename in os.listdir(images_folder):
        if filename.endswith(('.png', '.jpg', '.jpeg')) and not filename.startswith(
                'taulia-logo') and not filename.startswith('background'):
            content += f"- {filename}\n"

    # Send the message to the assistant
    send_message(client, conversation, assistant_id, content)

    # Wait for the response
    response = None
    while response is None:
        response = get_assistant_response(client, conversation, last_message_timestamp)
        time.sleep(2)  # Adding sleep to avoid rapid polling

    return response.dict()['content'][0]['text']['value']


def download_industry_image(industry, download_folder):
    downloader.download(industry, limit=1, output_dir=download_folder, adult_filter_off=True, force_replace=False, timeout=60)
    downloaded_images = os.listdir(os.path.join(download_folder, industry))
    return os.path.join(download_folder, industry, downloaded_images[0]) if downloaded_images else None


def add_title_slide(prs, logo_path, background_path):
    slide_layout = prs.slide_layouts[5]
    slide = prs.slides.add_slide(slide_layout)

    left = Inches(0)
    top = Inches(0)
    slide_width = prs.slide_width
    slide_height = prs.slide_height
    slide.shapes.add_picture(background_path, left, top, width=slide_width, height=slide_height)

    logo_left = Inches(7.75)
    logo_top = Inches(0.5)
    logo_height = Inches(0.4)
    slide.shapes.add_picture(logo_path, logo_left, logo_top, height=logo_height)

    title_placeholder = buyer_name
    subtitle_placeholder = "Terms Extension Opportunity Assessment June 24"

    # Create a textbox for the title with a solid background
    text_left = Inches(1)
    text_top = Inches(3)
    text_width = Inches(8)
    text_height = Inches(1)
    title_box = slide.shapes.add_textbox(text_left, text_top, text_width, text_height)
    title_frame = title_box.text_frame
    title_frame.text = title_placeholder
    title_frame.paragraphs[0].font.size = Pt(32)
    title_frame.paragraphs[0].font.bold = True
    title_frame.paragraphs[0].font.color.rgb = RGBColor(255, 255, 255)  # White color
    title_frame.paragraphs[0].alignment = PP_PARAGRAPH_ALIGNMENT.CENTER

    # Set background color for the title box
    fill = title_box.fill
    fill.solid()
    fill.fore_color.rgb = RGBColor(0, 0, 0)  # Black color

    # Create a textbox for the subtitle with a solid background
    text_top = Inches(4)
    subtitle_box = slide.shapes.add_textbox(text_left, text_top, text_width, text_height)
    subtitle_frame = subtitle_box.text_frame
    subtitle_frame.text = subtitle_placeholder
    subtitle_frame.paragraphs[0].font.size = Pt(24)
    subtitle_frame.paragraphs[0].font.color.rgb = RGBColor(255, 255, 255)  # White color
    subtitle_frame.paragraphs[0].alignment = PP_PARAGRAPH_ALIGNMENT.CENTER

    # Set background color for the subtitle box
    fill = subtitle_box.fill
    fill.solid()
    fill.fore_color.rgb = RGBColor(0, 0, 0)  # Black color


def add_footer(prs, slide):
    slide_width = prs.slide_width

    footer_text = "© 2023 Taulia LLC. Confidential information. Do not distribute."
    footer_box = slide.shapes.add_textbox(Inches(0.5), prs.slide_height - Inches(0.22), slide_width / 2 - Inches(0.5),
                                          Inches(0.5))
    footer_frame = footer_box.text_frame
    footer_frame.text = footer_text
    footer_frame.paragraphs[0].font.size = Pt(10)
    footer_frame.paragraphs[0].alignment = PP_PARAGRAPH_ALIGNMENT.LEFT

    bar_left = slide_width / 2
    bar_top = prs.slide_height - Inches(0.15)
    bar_width = slide_width / 2
    bar_height = Inches(0.15)
    bar = slide.shapes.add_shape(1, bar_left, bar_top, bar_width, bar_height)
    fill = bar.fill
    fill.solid()
    fill.fore_color.rgb = RGBColor(255, 102, 0)
    bar.line.fill.background()


def add_summary_slide(prs, summary):
    slide_layout = prs.slide_layouts[5]
    slide = prs.slides.add_slide(slide_layout)

    text_left = Inches(1)
    text_top = Inches(1)
    text_width = prs.slide_width - Inches(2)
    text_height = prs.slide_height - Inches(2)
    text_box = slide.shapes.add_textbox(text_left, text_top, text_width, text_height)
    text_frame = text_box.text_frame
    text_frame.text = summary
    text_frame.word_wrap = True

    for paragraph in text_frame.paragraphs:
        paragraph.font.size = Pt(11)
        paragraph.alignment = PP_PARAGRAPH_ALIGNMENT.LEFT

    add_footer(prs, slide)


def add_content_slide(prs, title, img_path, logo_path):
    slide_layout = prs.slide_layouts[5]
    slide = prs.slides.add_slide(slide_layout)

    title_box = slide.shapes.title
    title_box.text = title

    # Set the font size for the title
    for paragraph in title_box.text_frame.paragraphs:
        paragraph.font.size = Pt(20)  # Adjust the font size as needed

    left = Inches(1)
    top = Inches(1.5)
    height = Inches(5)
    slide.shapes.add_picture(img_path, left, top, height=height)

    logo_height = Inches(0.3)
    slide_width = prs.slide_width
    logo_left = slide_width - Inches(2)
    logo_top = Inches(0.4)
    slide.shapes.add_picture(logo_path, logo_left, logo_top, height=logo_height)

    add_footer(prs, slide)


def create_ppt(images_folder, output_ppt, logo_path, assistant_name, buyer_industry):
    prs = Presentation()

    background_path = download_industry_image(buyer_industry, images_folder)
    if not background_path:
        print("Error: Unable to download background image. Using default background.")
        background_path = os.path.join(images_folder, 'background.jpg')

    add_title_slide(prs, logo_path, background_path)

    summary = get_summary_from_assistant(openai, assistant_name, images_folder, buyer_name)

    add_summary_slide(prs, summary)

    for filename in os.listdir(images_folder):
        if filename.endswith(('.png', '.jpg', '.jpeg')) and not filename.startswith(
                'taulia-logo') and not filename.startswith('background'):
            slide_title = os.path.splitext(filename)[0]
            img_path = os.path.join(images_folder, filename)
            add_content_slide(prs, slide_title, img_path, logo_path)

    try:
        prs.save(output_ppt)
        print(f"Presentation saved as {output_ppt}")
    except Exception as e:
        print(f"Error saving presentation: {e}")


# Paths and assistant name
images_folder = 'images'
logo_path = os.path.join(images_folder, 'taulia-logo.png')
output_ppt = f'presentations/opportunity_deck_{buyer_name}.pptx'
assistant_name = 'Presentation Generator'

create_ppt(images_folder, output_ppt, logo_path, assistant_name, buyer_industry)
