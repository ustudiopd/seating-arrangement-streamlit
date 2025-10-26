import streamlit as st
import pandas as pd
import json
from typing import List, Dict, Tuple
import random
from utils.seating_algorithm import generate_seating_arrangement
from utils.excel_export import create_excel_data, create_excel_file
from utils.data_manager import create_data_package, save_data_to_json, load_data_from_json, validate_data_package

# 페이지 설정
st.set_page_config(
    page_title="자리배치 프로그램",
    page_icon="🏫",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 세션 상태 초기화
if 'students' not in st.session_state:
    st.session_state.students = []
if 'seating_arrangement' not in st.session_state:
    st.session_state.seating_arrangement = {}
if 'pre_assigned_seats' not in st.session_state:
    st.session_state.pre_assigned_seats = {}
if 'disabled_seats' not in st.session_state:
    st.session_state.disabled_seats = []
if 'distanced_students' not in st.session_state:
    st.session_state.distanced_students = []
if 'layout_type' not in st.session_state:
    st.session_state.layout_type = 'default'
if 'rows' not in st.session_state:
    st.session_state.rows = 5
if 'cols' not in st.session_state:
    st.session_state.cols = 6
if 'is_teacher_view' not in st.session_state:
    st.session_state.is_teacher_view = False

def render_seating_grid(layout_type: str, rows: int, cols: int, seating_arrangement: Dict[int, str], is_teacher_view: bool = False):
    """자리 배치 그리드 렌더링"""
    if layout_type == 'pairs':
        # 짝꿍형 배치
        sections = rows
        rows_per_section = cols
        
        for s in range(sections):
            section_label = f'{sections - s}분단' if is_teacher_view else f'{s + 1}분단'
            st.subheader(f"{section_label}")
            
            cols_container = st.columns(2)
            
            for r in range(rows_per_section):
                read_row = rows_per_section - 1 - r if is_teacher_view else r
                
                left_index = (s * rows_per_section * 2) + (read_row * 2)
                right_index = left_index + 1
                
                if is_teacher_view:
                    left_index, right_index = right_index, left_index
                
                left_student = seating_arrangement.get(left_index, '')
                right_student = seating_arrangement.get(right_index, '')
                
                with cols_container[0]:
                    st.write(f"**{r + 1}행 왼쪽**")
                    st.info(left_student if left_student else "빈 자리")
                
                with cols_container[1]:
                    st.write(f"**{r + 1}행 오른쪽**")
                    st.info(right_student if right_student else "빈 자리")
    else:
        # 기본형 배치
        for r in range(rows):
            row_label = f'{rows - r}행' if is_teacher_view else f'{r + 1}행'
            st.subheader(f"{row_label}")
            
            cols_container = st.columns(cols)
            
            for c in range(cols):
                read_row = rows - 1 - r if is_teacher_view else r
                read_col = cols - 1 - c if is_teacher_view else c
                
                index = read_row * cols + read_col
                student = seating_arrangement.get(index, '')
                
                with cols_container[c]:
                    col_label = f'{cols - c}열' if is_teacher_view else f'{c + 1}열'
                    st.write(f"**{col_label}**")
                    st.info(student if student else "빈 자리")

def main():
    st.title("🏫 자리배치 프로그램")
    st.markdown("간편하고 빠른 자리 배치로 교실 분위기를 새롭게!")
    
    # 메인 레이아웃
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.header("1. 명단 입력")
        
        # 명단 입력
        name_input = st.text_area(
            "학생 명단",
            value="\n".join(st.session_state.students),
            height=150,
            placeholder="이름을 한 줄에 한 명씩 입력하세요.\n예시)\n김자두\n백레몬\n홍석류"
        )
        
        # 명단 업데이트
        if name_input:
            students = [name.strip() for name in name_input.split('\n') if name.strip()]
            st.session_state.students = students
        else:
            st.session_state.students = []
        
        st.write(f"총 {len(st.session_state.students)}명")
        
        # 그룹명 입력
        group_name = st.text_input("그룹명", placeholder="예: 3-4 (27명)")
        
        # 파일 저장/불러오기
        st.subheader("데이터 관리")
        
        col_save, col_load = st.columns(2)
        
        with col_save:
            if st.button("💾 저장"):
                if group_name and st.session_state.students:
                    data_package = create_data_package(
                        st.session_state.students,
                        st.session_state.layout_type,
                        st.session_state.rows,
                        st.session_state.cols,
                        st.session_state.pre_assigned_seats,
                        st.session_state.disabled_seats,
                        st.session_state.distanced_students,
                        group_name
                    )
                    
                    json_data = save_data_to_json(data_package)
                    filename = f"{group_name}_자리배치설정.json"
                    
                    st.download_button(
                        label="📥 다운로드",
                        data=json_data,
                        file_name=filename,
                        mime="application/json"
                    )
                else:
                    st.error("그룹명과 학생 명단을 입력해주세요.")
        
        with col_load:
            uploaded_file = st.file_uploader("📤 불러오기", type=['json'])
            if uploaded_file:
                try:
                    json_data = uploaded_file.read().decode('utf-8')
                    data = load_data_from_json(json_data)
                    
                    if validate_data_package(data):
                        st.session_state.students = data['students']
                        st.session_state.layout_type = data['layout_type']
                        st.session_state.rows = data['rows']
                        st.session_state.cols = data['cols']
                        st.session_state.pre_assigned_seats = data['pre_assigned_seats']
                        st.session_state.disabled_seats = data['disabled_seats']
                        st.session_state.distanced_students = data['distanced_students']
                        st.success(f"'{data['group_name']}' 그룹을 불러왔습니다.")
                        st.rerun()
                    else:
                        st.error("잘못된 파일 형식입니다.")
                except Exception as e:
                    st.error(f"파일 로드 오류: {e}")
        
        st.header("2. 책상 배열 설정")
        
        # 배치 유형 선택
        layout_type = st.selectbox(
            "배치 유형",
            ["default", "pairs"],
            format_func=lambda x: "기본형" if x == "default" else "짝꿍형 (분단형)",
            index=0 if st.session_state.layout_type == "default" else 1
        )
        st.session_state.layout_type = layout_type
        
        # 행/열 설정
        col_rows, col_cols = st.columns(2)
        
        with col_rows:
            if layout_type == "pairs":
                rows = st.number_input("분단 수", min_value=1, max_value=10, value=st.session_state.rows)
                cols = st.number_input("행 수", min_value=1, max_value=10, value=st.session_state.cols)
            else:
                rows = st.number_input("행 (가로)", min_value=1, max_value=15, value=st.session_state.rows)
                cols = st.number_input("열 (세로)", min_value=1, max_value=15, value=st.session_state.cols)
        
        st.session_state.rows = rows
        st.session_state.cols = cols
        
        # 배열 적용 버튼
        if st.button("배열 적용"):
            st.session_state.seating_arrangement = {}
            st.success("배열이 적용되었습니다.")
        
        # 고급 설정
        with st.expander("🔧 고급 설정"):
            st.subheader("사전 자리 지정")
            
            if st.session_state.students:
                selected_student = st.selectbox(
                    "학생 선택",
                    [""] + st.session_state.students,
                    key="pre_assign_student"
                )
                
                if selected_student:
                    # 사용 가능한 자리 목록 생성
                    if layout_type == 'pairs':
                        total_seats = rows * cols * 2
                    else:
                        total_seats = rows * cols
                    
                    available_seats = []
                    for i in range(total_seats):
                        if i not in st.session_state.disabled_seats:
                            seat_label = f"{i + 1}번 자리"
                            available_seats.append((seat_label, i))
                    
                    if available_seats:
                        selected_seat_label = st.selectbox(
                            "자리 선택",
                            [""] + [seat[0] for seat in available_seats],
                            key="pre_assign_seat"
                        )
                        
                        if selected_seat_label and st.button("지정"):
                            seat_index = next(seat[1] for seat in available_seats if seat[0] == selected_seat_label)
                            st.session_state.pre_assigned_seats[seat_index] = selected_student
                            st.success(f"{selected_student} 학생을 {selected_seat_label}에 지정했습니다.")
                    else:
                        st.warning("사용 가능한 자리가 없습니다.")
            
            st.subheader("자리 띄우기")
            
            if st.session_state.students:
                distanced_students = st.multiselect(
                    "자리를 띄워야 하는 학생들",
                    st.session_state.students,
                    default=st.session_state.distanced_students
                )
                st.session_state.distanced_students = distanced_students
                
                if distanced_students:
                    st.info(f"선택된 학생들: {', '.join(distanced_students)}")
        
        # 자리 배치 생성
        if st.button("🎲 자리 바꾸기!", type="primary"):
            if st.session_state.students:
                with st.spinner("자리 배치 중..."):
                    st.session_state.seating_arrangement = generate_seating_arrangement(
                        st.session_state.students,
                        st.session_state.layout_type,
                        st.session_state.rows,
                        st.session_state.cols,
                        st.session_state.pre_assigned_seats,
                        st.session_state.disabled_seats,
                        st.session_state.distanced_students
                    )
                st.success("자리 배치가 완료되었습니다!")
            else:
                st.error("학생 명단을 먼저 입력해주세요.")
        
        # 초기화 버튼
        if st.button("🗑️ 모두 지우기"):
            st.session_state.seating_arrangement = {}
            st.session_state.pre_assigned_seats = {}
            st.session_state.disabled_seats = []
            st.session_state.distanced_students = []
            st.success("모든 설정이 초기화되었습니다.")
        
    with col2:
        st.header("3. 자리 배치 결과")
        
        # 교사 기준 보기 토글
        col_toggle, col_download = st.columns([1, 1])
        
        with col_toggle:
            if st.button("👨‍🏫 교사 기준 보기" if not st.session_state.is_teacher_view else "👨‍🎓 학생 기준 보기"):
                st.session_state.is_teacher_view = not st.session_state.is_teacher_view
                st.rerun()
        
        with col_download:
            if st.session_state.seating_arrangement:
                excel_data = create_excel_data(
                    st.session_state.seating_arrangement,
                    st.session_state.layout_type,
                    st.session_state.rows,
                    st.session_state.cols,
                    st.session_state.is_teacher_view
                )
                
                excel_file = create_excel_file(excel_data)
                filename = "자리배치결과(교사기준).xlsx" if st.session_state.is_teacher_view else "자리배치결과(학생기준).xlsx"
                
                st.download_button(
                    label="📊 엑셀 다운로드",
                    data=excel_file,
                    file_name=filename,
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                )
        
        # 자리 배치 결과 표시
        if st.session_state.seating_arrangement:
            st.subheader("교탁")
            st.markdown("---")
            
            render_seating_grid(
                st.session_state.layout_type,
                st.session_state.rows,
                st.session_state.cols,
                st.session_state.seating_arrangement,
                st.session_state.is_teacher_view
            )
        else:
            st.info("자리 배치를 생성하려면 '자리 바꾸기!' 버튼을 클릭하세요.")
        
        # 사용법 안내
        with st.expander("📖 사용법 안내"):
            st.markdown("""
            ### 기본 사용법
            1. **명단 입력**: 학생 이름을 한 줄에 한 명씩 입력
            2. **배치 설정**: 원하는 책상 배열 유형과 크기 설정
            3. **자리 배치**: '자리 바꾸기!' 버튼으로 랜덤 배치 생성
            4. **결과 확인**: 교사/학생 기준으로 보기 전환 가능
            5. **엑셀 저장**: 결과를 엑셀 파일로 다운로드
            
            ### 고급 기능
            - **사전 자리 지정**: 특정 학생을 원하는 자리에 고정
            - **자리 띄우기**: 선택한 학생들이 서로 붙어 앉지 않도록 설정
            - **데이터 저장**: 설정을 JSON 파일로 저장하여 나중에 불러오기 가능
            """)

if __name__ == "__main__":
    main()
