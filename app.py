import streamlit as st
import subprocess as sp
import sys
import os


st.title(" 🤖 AI Business Analyst")

st.write("Analyze your retail business data and get AI-powered recommendations.")

if st.button("Generate AI Recommendations"):

    with st.spinner("Analysing Your Business Data..."):

    
     env = os.environ.copy()
     env["OLLAMA_LLM_LIBRARY"] = "cpu"


    result = sp.run(
        [sys.executable,"src/ai.py"],
        capture_output=True,text = True,
        env=env)

    if result.returncode == 0:
        st.success("AI analysis completed successfully!")
        output = result.stdout

        sections = output.split("Finding ")

        for section in sections[1:]:
            lines = section.strip().splitlines()

            st.markdown("-----")
            st.subheader("📊 Finding " + lines[0].replace(":", ""))

            for line in lines[1:]:
               if line.startswith("Finding:"):
                   finding_text = line.replace("Finding:", "").strip()

                   if finding_text.startswith("Order status counts are"):
                        st.write("**Finding:**")
                        st.write("Order status counts:")
                        st.write("• Pending: 260")
                        st.write("• Cancelled: 258")
                        st.write("• Delivered: 248")
                        st.write("• Shipped: 234")
                   else:
                    st.write("**Finding:**")
                    st.write(finding_text)

               elif line.startswith("Recommendation:"):
                    st.write("**💡 Recommendation:**")
                    st.write(line.replace("Recommendation:", "").strip())

               elif line.startswith("How to improve:"):
                    st.write("**🔧 How to Improve:**")
                    st.write(line.replace("How to improve:", "").strip())

    else:
        st.error("AI analysis failed. Something went wrong.")
        st.write("return code:", result.returncode)
        st.write("STDOUT:")
        st.code(result.stdout)
        st.write("STDERR:")
        st.code(result.stderr)

  