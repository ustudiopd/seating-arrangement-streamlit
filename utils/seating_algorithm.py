"""
자리 배치 알고리즘 모듈
"""
import random
from typing import List, Dict, Tuple

def get_seat_coordinates(index: int, layout_type: str, rows: int, cols: int) -> Tuple[int, int]:
    """자리 인덱스를 좌표로 변환"""
    if layout_type == 'pairs':
        # 짝꿍형 배치의 경우
        rows_per_section = rows
        desks_per_section = rows_per_section * 2
        section = index // desks_per_section
        index_in_section = index % desks_per_section
        row = index_in_section // 2
        col = (section * 2) + (index_in_section % 2)
        return row, col
    else:
        # 기본형 배치의 경우
        row = index // cols
        col = index % cols
        return row, col

def is_too_close(index1: int, index2: int, layout_type: str, rows: int, cols: int) -> bool:
    """두 자리가 너무 가까운지 확인"""
    pos1 = get_seat_coordinates(index1, layout_type, rows, cols)
    pos2 = get_seat_coordinates(index2, layout_type, rows, cols)
    
    # 인접한 자리 체크 (상하좌우 + 대각선)
    if abs(pos1[0] - pos2[0]) <= 1 and abs(pos1[1] - pos2[1]) <= 1:
        return True
    
    # 같은 행에서 2칸 이내
    if pos1[0] == pos2[0] and abs(pos1[1] - pos2[1]) <= 2:
        return True
    
    # 같은 열에서 2칸 이내
    if pos1[1] == pos2[1] and abs(pos1[0] - pos2[0]) <= 2:
        return True
    
    return False

def generate_seating_arrangement(
    students: List[str],
    layout_type: str,
    rows: int,
    cols: int,
    pre_assigned_seats: Dict[int, str] = None,
    disabled_seats: List[int] = None,
    distanced_students: List[str] = None
) -> Dict[int, str]:
    """
    자리 배치 생성
    
    Args:
        students: 학생 명단
        layout_type: 배치 유형 ('default' 또는 'pairs')
        rows: 행 수
        cols: 열 수
        pre_assigned_seats: 사전 지정된 자리 {자리인덱스: 학생명}
        disabled_seats: 비활성화된 자리 인덱스 리스트
        distanced_students: 자리를 띄워야 하는 학생들
    
    Returns:
        자리 배치 결과 {자리인덱스: 학생명}
    """
    if pre_assigned_seats is None:
        pre_assigned_seats = {}
    if disabled_seats is None:
        disabled_seats = []
    if distanced_students is None:
        distanced_students = []
    
    # 전체 자리 수 계산
    if layout_type == 'pairs':
        total_seats = rows * cols * 2
    else:
        total_seats = rows * cols
    
    # 사용 가능한 자리 계산
    available_seats = []
    for i in range(total_seats):
        if i not in disabled_seats and i not in pre_assigned_seats:
            available_seats.append(i)
    
    # 사전 지정된 학생들 제외
    pre_assigned_students = set(pre_assigned_seats.values())
    regular_students = [s for s in students if s not in pre_assigned_students]
    
    # 자리 띄우기 대상 학생들 처리
    distanced_students = [s for s in distanced_students if s not in pre_assigned_students]
    
    # 결과 초기화
    result = pre_assigned_seats.copy()
    placed_distanced_indices = []
    unplaced_distanced = []
    
    # 1. 자리 띄우기 대상 학생들 배치
    if distanced_students:
        shuffled_available = available_seats.copy()
        random.shuffle(shuffled_available)
        
        for student in distanced_students:
            placed = False
            for i, seat_index in enumerate(shuffled_available):
                # 다른 자리 띄우기 대상 학생들과 너무 가까운지 확인
                too_close = any(is_too_close(seat_index, placed_idx, layout_type, rows, cols) 
                              for placed_idx in placed_distanced_indices)
                
                if not too_close:
                    result[seat_index] = student
                    placed_distanced_indices.append(seat_index)
                    shuffled_available.pop(i)
                    placed = True
                    break
            
            if not placed:
                unplaced_distanced.append(student)
        
        # 사용 가능한 자리 업데이트
        available_seats = shuffled_available
    
    # 자리 띄우기에 실패한 학생들을 일반 학생 그룹에 추가
    regular_students.extend(unplaced_distanced)
    
    # 2. 일반 학생들 배치
    random.shuffle(regular_students)
    
    for i, student in enumerate(regular_students):
        if i < len(available_seats):
            result[available_seats[i]] = student
    
    return result