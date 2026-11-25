import hashlib
import tempfile
from pathlib import Path

import streamlit as st
from src.bellara_scanner import scan

st.set_page_config(page_title='Bellara Scanner', page_icon='📐', layout='wide')
st.title('Bellara Scanner')
st.caption('Automatic panel recognition system')

with st.sidebar:
    st.header('Settings')
    first = st.selectbox('First panel', ['Auto', 'S', 'M', 'L'], index=3)
    st.divider()
    st.write('S — 90 mm')
    st.write('M — 135 mm')
    st.write('L — 200 mm')

panel_width = st.number_input(
    'Panel width (mm)',
    min_value=0.0,
    value=3000.0,
    step=0.1,
    format='%.2f',
    help='Enter the total panel width in millimeters',
)

uploaded_file = st.file_uploader(
    'Upload drawing or photo', type=['jpg', 'jpeg', 'png']
)

# Clear stale results when the image or first-panel setting changes.
image_bytes = uploaded_file.getvalue() if uploaded_file is not None else None
scan_key = (hashlib.sha256(image_bytes).hexdigest(), first) if image_bytes else None
if st.session_state.get('scan_key') != scan_key:
    st.session_state.pop('result', None)
    st.session_state.pop('marked_image', None)
    st.session_state['scan_key'] = scan_key

if uploaded_file is not None:
    st.subheader('Original image')
    st.image(image_bytes, use_container_width=True)

    if st.button('Scan image', type='primary', use_container_width=True):
        try:
            with st.spinner('Processing image...'):
                with tempfile.TemporaryDirectory() as temp:
                    suffix = Path(uploaded_file.name).suffix.lower()
                    file_path = Path(temp) / f'image{suffix}'
                    file_path.write_bytes(image_bytes)

                    result = scan(str(file_path), first=None if first == 'Auto' else first)
                    marked_image = Path(result['output']).read_bytes()
                    result.pop('output', None)  # Temporary file is deleted after processing.
                    st.session_state['result'] = result
                    st.session_state['marked_image'] = marked_image
        except Exception as e:
            st.session_state.pop('result', None)
            st.session_state.pop('marked_image', None)
            st.error(str(e))

if uploaded_file is not None and 'result' in st.session_state:
    result = st.session_state['result']
    # Width is a user input, not a scanner calibration parameter.
    # Update it immediately without rescanning the image.
    result['panel_width'] = panel_width
    sequence = result['sequence']
    counts = result['counts']

    st.divider()
    st.subheader('Processed image')
    st.image(st.session_state['marked_image'], use_container_width=True)

    col1, col2, col3, col4, col5 = st.columns(5)
    col1.metric('Small', counts.get('S', 0))
    col2.metric('Medium', counts.get('M', 0))
    col3.metric('Large', counts.get('L', 0))
    col4.metric('Total', len(sequence))
    col5.metric('Panel width', f'{panel_width:.2f} mm')

    st.subheader('Detected sequence')
    st.code(sequence, language=None)
    st.caption(f"Valid scan lines: {result['scan_lines']}/19")

    if '?' in sequence:
        st.warning('Some panels require manual confirmation.')

    col1, col2 = st.columns(2)
    with col1:
        st.download_button(
            'Download processed image', data=st.session_state['marked_image'],
            file_name='bellara_marked.png', mime='image/png', use_container_width=True,
        )
    with col2:
        st.download_button(
            'Download sequence', data=sequence, file_name='sequence.txt',
            mime='text/plain', use_container_width=True,
        )

    with st.expander('Debug information'):
        st.json(result)
