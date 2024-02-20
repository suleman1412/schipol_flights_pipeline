import streamlit as st
class TopAircraftsSection:
    def __init__(self, aircrafts_df):
        self.aircrafts_df = aircrafts_df

    def generate_aircrafts_html(self, index):
        aircrafts = self.aircrafts_df.iloc[index]
        
        def get_position(index):
            if index == 1:
                position = f"{index}st"
            elif index == 2:
                position = f"{index}nd"
            elif index == 3:
                position = f"{index}rd"
            else:
                position = f"{index}th"
            return position

        return [
            f"<img style='display: block; margin-left: auto; margin-right: auto; width: 150px;' src='{aircrafts.iloc[0]}'/>",
            f"<p style='text-align: center; padding-top: 0.8rem;'><b>{get_position(index + 1)}:</b> {aircrafts.iloc[1]}</p>",
            f"<p style='text-align: center;'><b>Count:</b> {aircrafts.iloc[2]}</p>"
        ]

    def display(self):
        with st.container():
            st.subheader("Top 5 arriving aircrafts")
            columns = st.columns(5)

            for i, col in enumerate(columns):
                with col:
                    markdown_list = self.generate_aircrafts_html(i)
                    for item in markdown_list:
                        st.markdown(item, unsafe_allow_html=True)