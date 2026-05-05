import xlsxwriter
import json
from mitmproxy import http

# Global variables for Excel writing
workbook = None
worksheet = None
row = 0

def setup():
    global workbook, worksheet
    # Open an Excel file for writing
    workbook = xlsxwriter.Workbook('analytics_events.xlsx')
    worksheet = workbook.add_worksheet()
    # Write headers
    worksheet.write(0, 0, 'Event Type')
    worksheet.write(0, 1, 'Timestamp')
    worksheet.write(0, 2, 'URL')
    worksheet.write(0, 3, 'Payload')

def done():
    global workbook
    if workbook:
        workbook.close()

def request(flow: http.HTTPFlow) -> None:
    # Check if the request is from the analytics endpoint
    if flow.request.pretty_url.startswith('https://analytics.santabrowser.com'):
        global row, worksheet
        if worksheet:
            row += 1
            try:
                # Try to parse JSON payload
                payload = json.loads(flow.request.text) if flow.request.text else {}

                event_type = payload.get('event', 'Unknown')
                timestamp = payload.get('timestamp', 'Unknown')

                # Write to Excel
                worksheet.write(row, 0, event_type)
                worksheet.write(row, 1, str(timestamp))
                worksheet.write(row, 2, flow.request.pretty_url)
                worksheet.write(row, 3, json.dumps(payload))

                print(f"Captured analytics event: {event_type} at {timestamp}")

            except Exception as e:
                print(f"Error processing analytics request: {e}")
                worksheet.write(row, 0, 'Error')
                worksheet.write(row, 1, str(e))
                worksheet.write(row, 2, flow.request.pretty_url)
                worksheet.write(row, 3, flow.request.text[:500])  # First 500 chars