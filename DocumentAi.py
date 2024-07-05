from google.api_core.client_options import ClientOptions
from google.cloud import documentai
import os

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = "cac-document-ai-423407-bd90b5b0ffe7.json"

project_id = "cac-document-ai-423407"
location = "us"  # Format is "us" or "eu"
file_path = "./SiteVisit1.jpg"
processor_display_name = "CACFormParser"  # Must be unique per project, e.g.: "My Processor"

def quickstart(
    project_id: str,
    location: str,
    file_path: str,
    processor_display_name: str = "My Processor",
):
    # You must set the `api_endpoint` if you use a location other than "us".
    opts = ClientOptions(api_endpoint=f"{location}-documentai.googleapis.com")
    client = documentai.DocumentProcessorServiceClient(client_options=opts)

    # The full resource name of the location, e.g.:
    # `projects/{project_id}/locations/{location}`
    parent = client.common_location_path(project_id, location)

    processor = ""  # Initialize processor variable here

    try:
        # Try to create the processor
        processor = client.create_processor(
            parent=parent,
            processor=documentai.Processor(
                type_="FORM_PARSER_PROCESSOR",  # Refer to https://cloud.google.com/document-ai/docs/create-processor for how to get available processor types
                display_name=processor_display_name,
            ),
        )
        print(f"Processor Name: {processor.name}")
        processorExecute = True

    except Exception as e:
        processors = client.list_processors(parent=parent)
        for p in processors:
            if p.display_name == processor_display_name:
                processor = p
                print(f"Processor '{processor_display_name}' already exists.")
                break
        processorExecute = True

    if processorExecute:
        # Read the file into memory
        print("processor")
        with open(file_path, "rb") as image:
            image_content = image.read()

        # Load binary data
        raw_document = documentai.RawDocument(
            content=image_content,
            mime_type="image/jpeg",  # Refer to https://cloud.google.com/document-ai/docs/file-types for supported file types
        )
        request = documentai.ProcessRequest(name=processor.name, raw_document=raw_document)

        result = client.process_document(request=request)

        # For a full list of `Document` object attributes, reference this page:
        # https://cloud.google.com/document-ai/docs/reference/rest/v1/Document
        document = result.document

        # Read the text recognition output from the processor
        print("The document contains the following text:")
        print(document.text)

quickstart(project_id, location, file_path, processor_display_name)
