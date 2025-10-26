"""
엑셀 다운로드 기능 모듈
"""
import pandas as pd
from typing import Dict, List

def create_excel_data(
    seating_arrangement: Dict[int, str],
    layout_type: str,
    rows: int,
    cols: int,
    is_teacher_view: bool = False
) -> List[List[str]]:
    """
    자리 배치 데이터를 엑셀 형식으로 변환
    
    Args:
        seating_arrangement: 자리 배치 결과 {자리인덱스: 학생명}
        layout_type: 배치 유형 ('default' 또는 'pairs')
        rows: 행 수
        cols: 열 수
        is_teacher_view: 교사 기준 보기 여부
    
    Returns:
        엑셀 데이터 (2차원 리스트)
    """
    data = []
    
    if layout_type == 'pairs':
        # 짝꿍형 배치
        sections = rows
        rows_per_section = cols
        
        # 헤더 생성
        header1 = ['']
        header2 = ['행']
        for s in range(sections):
            section_label = f'{sections - s}분단' if is_teacher_view else f'{s + 1}분단'
            header1.extend([section_label, ''])
            header2.extend(['왼쪽', '오른쪽'])
        
        data.append(header1)
        data.append(header2)
        
        # 데이터 행 생성
        for r in range(rows_per_section):
            row_label = f'{rows_per_section - r}행' if is_teacher_view else f'{r + 1}행'
            row_data = [row_label]
            
            for s in range(sections):
                read_section = sections - 1 - s if is_teacher_view else s
                read_row = rows_per_section - 1 - r if is_teacher_view else r
                
                student_left_index = (read_section * rows_per_section * 2) + (read_row * 2)
                student_right_index = student_left_index + 1
                
                left_index = student_right_index if is_teacher_view else student_left_index
                right_index = student_left_index if is_teacher_view else student_right_index
                
                left_student = seating_arrangement.get(left_index, '')
                right_student = seating_arrangement.get(right_index, '')
                
                row_data.extend([left_student, right_student])
            
            data.append(row_data)
    
    else:
        # 기본형 배치
        # 헤더 생성
        header = [' ']
        for c in range(cols):
            col_label = f'{cols - c}열' if is_teacher_view else f'{c + 1}열'
            header.append(col_label)
        data.append(header)
        
        # 데이터 행 생성
        for r in range(rows):
            row_label = f'{rows - r}행' if is_teacher_view else f'{r + 1}행'
            row_data = [row_label]
            
            for c in range(cols):
                read_row = rows - 1 - r if is_teacher_view else r
                read_col = cols - 1 - c if is_teacher_view else c
                
                index = read_row * cols + read_col
                student = seating_arrangement.get(index, '')
                row_data.append(student)
            
            data.append(row_data)
    
    return data

def create_excel_file(data: List[List[str]], filename: str = "자리배치결과.xlsx") -> bytes:
    """
    엑셀 파일 생성
    
    Args:
        data: 엑셀 데이터
        filename: 파일명
    
    Returns:
        엑셀 파일 바이트 데이터
    """
    df = pd.DataFrame(data)
    
    # 엑셀 파일 생성
    from io import BytesIO
    output = BytesIO()
    
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, sheet_name='자리배치도', index=False, header=False)
        
        # 열 너비 자동 조정
        worksheet = writer.sheets['자리배치도']
        for column in worksheet.columns:
            max_length = 0
            column_letter = column[0].column_letter
            
            for cell in column:
                try:
                    if len(str(cell.value)) > max_length:
                        max_length = len(str(cell.value))
                except:
                    pass
            
            adjusted_width = min(max_length + 2, 20)
            worksheet.column_dimensions[column_letter].width = adjusted_width
    
    output.seek(0)
    return output.getvalue()