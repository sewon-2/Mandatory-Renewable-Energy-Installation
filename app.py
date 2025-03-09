import os
import gspread
import traceback
from flask import Flask, request, jsonify, render_template
from oauth2client.service_account import ServiceAccountCredentials

app = Flask(__name__)

# ✅ Google Drive API 인증 설정
SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]

# ✅ JSON 키 파일 경로 설정
JSON_KEYFILE = os.path.join(os.getcwd(), "xenon-anvil-452816-d3-5b8ee03e44bd.json")
print(f"[DEBUG] JSON 키 파일 경로: {JSON_KEYFILE}")

if not os.path.exists(JSON_KEYFILE):
    raise FileNotFoundError(f"JSON 키 파일이 존재하지 않습니다: {JSON_KEYFILE}")

# ✅ Google Sheets API 클라이언트 인증
CREDENTIALS = ServiceAccountCredentials.from_json_keyfile_name(JSON_KEYFILE, SCOPE)
CLIENT = gspread.authorize(CREDENTIALS)

# ✅ Google Sheets 파일 ID 설정
SPREADSHEET_ID = "1rr4Nz9s_ZkEzBu3hEf-a0-hvTT4tJzdx1zKZByVivUw"  # 실제 파일 ID 입력

def get_google_sheet():
    """Google Drive API를 사용하여 엑셀 데이터를 불러오는 함수"""
    try:
        print(f"[DEBUG] Google Sheet (파일 ID) 열기 시도: {SPREADSHEET_ID}")
        spreadsheet = CLIENT.open_by_key(SPREADSHEET_ID)
        print("[DEBUG] Google Sheet 연결 성공")
        return spreadsheet
    except gspread.exceptions.SpreadsheetNotFound:
        raise ValueError(f"[ERROR] Google Sheet 파일을 찾을 수 없습니다: {SPREADSHEET_ID}. "
                         "파일 ID가 정확한지 확인하고 서비스 계정에 공유되었는지 다시 확인하세요.")
    except Exception as e:
        error_details = traceback.format_exc()
        print(f"[ERROR] Google Sheet 연결 실패:\n{error_details}")
        raise

@app.route('/')
def index():
    try:
        spreadsheet = get_google_sheet()
        index_1_sheet = spreadsheet.worksheet("INDEX-1 (단위 에너지사용량)")
        index_2_sheet = spreadsheet.worksheet("INDEX-2 (지역계수)")
        index_3_sheet = spreadsheet.worksheet("INDEX-3 (단위 에너지생산량 및 원별 보정계수)")

        region_list = index_2_sheet.col_values(2)[3:20]  # 지역 목록
        building_use_list = index_1_sheet.col_values(3)[3:21]  # 건축 용도 목록
        energy_source_list = index_3_sheet.col_values(3)[2:21]  # 에너지원 목록

        return render_template(
            'index.html',
            region_list=region_list,
            building_use_list=building_use_list,
            energy_source_list=energy_source_list
        )
    except Exception as e:
        error_details = traceback.format_exc()
        print(f"[ERROR] 데이터 로딩 실패:\n{error_details}")
        return f"Error loading data: {str(e)}"

@app.route('/submit', methods=['POST'])
def submit_data():
    """웹에서 입력받은 데이터를 Google Drive 엑셀에 입력하고 연산된 결과를 반환하는 엔드포인트"""
    try:
        data = request.form
        spreadsheet = get_google_sheet()
        sheet = spreadsheet.worksheet("신, 재생에너지 공급 비율 (건축허가)")

        def safe_get(key, default=""):
            return data.get(key, default)

        sheet.update('B5', [[safe_get('region')]])
        sheet.update('A5', [[safe_get('building-use-1')]])
        sheet.update('A6', [[safe_get('building-use-2')]])
        sheet.update('A7', [[safe_get('building-use-3')]])
        sheet.update('C5', [[safe_get('total-area-1')]])
        sheet.update('C6', [[safe_get('total-area-2')]])
        sheet.update('C7', [[safe_get('total-area-3')]])
        sheet.update('H5', [[safe_get('energy-source-1')]])
        sheet.update('H6', [[safe_get('energy-source-2')]])
        sheet.update('H7', [[safe_get('energy-source-3')]])
        sheet.update('I5', [[safe_get('installation-size-1')]])
        sheet.update('I6', [[safe_get('installation-size-2')]])
        sheet.update('I7', [[safe_get('installation-size-3')]])

        def safe_read(cell):
            value = sheet.acell(cell).value
            return value if value is not None else "N/A"

        results = {
            "energy_source_1": safe_read('H5'),
            "energy_source_2": safe_read('H6'),
            "energy_source_3": safe_read('H7'),
            "production_1": safe_read('L5'),
            "production_2": safe_read('L6'),
            "production_3": safe_read('L7'),
            "supply_ratio_1": safe_read('F14'),
            "supply_ratio_2": safe_read('F15'),
            "supply_ratio_3": safe_read('F16'),
            "total_ratio": safe_read('F17'),
        }

        return jsonify({"message": "Data processed successfully", "results": results})

    except Exception as e:
        error_details = traceback.format_exc()
        print(f"[ERROR] 데이터 처리 중 문제 발생:\n{error_details}")
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
