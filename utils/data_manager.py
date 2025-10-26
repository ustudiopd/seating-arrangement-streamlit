"""
데이터 저장/불러오기 관리 모듈
"""
import json
from typing import Dict, List, Any

def create_data_package(
    students: List[str],
    layout_type: str,
    rows: int,
    cols: int,
    pre_assigned_seats: Dict[int, str],
    disabled_seats: List[int],
    distanced_students: List[str],
    group_name: str = ""
) -> Dict[str, Any]:
    """
    현재 설정을 JSON 패키지로 생성
    
    Args:
        students: 학생 명단
        layout_type: 배치 유형
        rows: 행 수
        cols: 열 수
        pre_assigned_seats: 사전 지정된 자리
        disabled_seats: 비활성화된 자리
        distanced_students: 자리 띄우기 대상 학생들
        group_name: 그룹명
    
    Returns:
        JSON 직렬화 가능한 데이터 패키지
    """
    return {
        "group_name": group_name,
        "students": students,
        "layout_type": layout_type,
        "rows": rows,
        "cols": cols,
        "pre_assigned_seats": pre_assigned_seats,
        "disabled_seats": disabled_seats,
        "distanced_students": distanced_students,
        "version": "1.0"
    }

def save_data_to_json(data_package: Dict[str, Any]) -> str:
    """
    데이터 패키지를 JSON 문자열로 변환
    
    Args:
        data_package: 저장할 데이터 패키지
    
    Returns:
        JSON 문자열
    """
    return json.dumps(data_package, ensure_ascii=False, indent=2)

def load_data_from_json(json_string: str) -> Dict[str, Any]:
    """
    JSON 문자열에서 데이터 패키지 로드
    
    Args:
        json_string: JSON 문자열
    
    Returns:
        데이터 패키지
    """
    try:
        data = json.loads(json_string)
        
        # 버전 호환성 체크
        if "version" not in data:
            data["version"] = "1.0"
        
        # 필수 필드 기본값 설정
        if "pre_assigned_seats" not in data:
            data["pre_assigned_seats"] = {}
        if "disabled_seats" not in data:
            data["disabled_seats"] = []
        if "distanced_students" not in data:
            data["distanced_students"] = []
        
        return data
    except json.JSONDecodeError as e:
        raise ValueError(f"JSON 파싱 오류: {e}")

def validate_data_package(data: Dict[str, Any]) -> bool:
    """
    데이터 패키지 유효성 검사
    
    Args:
        data: 검사할 데이터 패키지
    
    Returns:
        유효성 여부
    """
    required_fields = ["students", "layout_type", "rows", "cols"]
    
    for field in required_fields:
        if field not in data:
            return False
    
    # 타입 검사
    if not isinstance(data["students"], list):
        return False
    if not isinstance(data["rows"], int) or data["rows"] <= 0:
        return False
    if not isinstance(data["cols"], int) or data["cols"] <= 0:
        return False
    
    return True