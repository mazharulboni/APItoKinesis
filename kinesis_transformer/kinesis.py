import base64
import json
import logging
import datetime

logging.getLogger().setLevel(logging.INFO)


def lambda_handler(event, context):
    logging.info("Event from Kinesis: {}".format(event))
    output_records = []
    utc_now = datetime.datetime.utcnow()
    utc_formatted_current_time = utc_now.strftime('%Y-%m-%d %H:%M:%S')

    for record in event['records']:
        base64_payload = record['data']
        payload = base64.b64decode(record['data']).decode('utf-8')
        input_json = json.loads(payload)
        # Assuming the JSON structure has keys 'field1' and 'field2'
        identification_profile = input_json.get('identificationProfile').get('jobID')
        license_plate_no = input_json.get('identificationProfile').get('licensePlateNo')
        event_date_time = input_json.get('identificationProfile').get('eventDateTime')

        # payload_as_text = str(input_json)

        # csv_row = f'{utc_formatted_current_time},{identification_profile},{license_plate_no},{base64_payload}\n'
        csv_row = f'INSERT,toll_booth_camera_log,izaan,{event_date_time},{base64_payload}\n'

        logging.info("CSV ROW: {}".format(csv_row))
        # Create the CSV formatted record
        output_record = {
            'recordId': record['recordId'],
            'result': 'Ok',
            'data': base64.b64encode(csv_row.encode('utf-8')).decode('utf-8')
        }
        logging.info("Output Records: {}".format(output_record))
        output_records.append(output_record)

    return {'records': output_records}