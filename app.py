import streamlit as st
import groq
import logging
import time
from prompts import(build_summarize_prompt, build_topic_prompt)
from groq_client import get_notes

st.set_page_config(
    page_title="AI Notes Assistant",
    page_icon="🧠",
    layout="centered"
)

# -------------------------
# Session State
# -------------------------
if "page" not in st.session_state:
    st.session_state.page = "home"


# -------------------------
# Home Page
# -------------------------
if st.session_state.page == "home":

    st.title("🧠 AI Notes Assistant")
    st.write("### Choose a tool")

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("📄 Summarize Text")
        st.write("Paste your notes and generate a concise summary.")

        if st.button("Open", key="open_summarize", use_container_width=True):
            st.session_state.page = "summarize"
            st.rerun()

    with col2:
        st.subheader("💡 Generate from Topic")
        st.write("Generate notes from a topic or concept.")

        if st.button("Open", key="open_topic", use_container_width=True):
            st.session_state.page = "topic"
            st.rerun()


# -------------------------
# Summarize Page
# -------------------------
elif st.session_state.page == "summarize":

    st.title("📄 Summarize Text")

    raw_text = st.text_area(
        "Paste your text",
        height=250
    )

    user_instructions = st.text_area(
        "Additional Instructions (Optional)"
    )

    response = None

    col1, col2 = st.columns(2)

    with col1:
        back = st.button("⬅ Back", use_container_width=True)

    if back:
        st.session_state.page = "home"
        st.rerun()

    with col2:
        generate = st.button("Generate", use_container_width=True)

    if generate:
        st.divider()
        prompt = build_summarize_prompt(raw_text, user_instructions)

        with st.status("🤖 AI is working...", expanded=True) as status:
            st.write("📝 Understanding your request...")
            
            success = False
            try:
                start = time.time()
                response = get_notes(prompt)
                elapsed = time.time() - start
                success = True

                st.write("🧠 Generating notes...")
                st.write("✨ Formatting the response...")

                st.caption(f"⚡ Generated in {elapsed:.2f} seconds")

            except groq.AuthenticationError as e:
                logging.error(f"Auth error: {e}")
                st.error(":gray[⚠️ Invalid API key. Check your .env file.]")

            except groq.RateLimitError as e:
                logging.error(f"Rate limit: {e}")
                st.error(":gray[⚠️ Too many requests — please wait a moment and try again.]")

            except groq.APIConnectionError as e:
                logging.error(f"Connection error: {e}")
                st.error(":gray[⚠️ Unable to connect. Check your internet.]")

            except Exception as e:
                logging.error(f"Unexpected error: {e}")
                st.error(":gray[⚠️ Something went wrong. Please try again.]")

            finally:
                if success:
                    status.update(
                        label="✅ Notes generated successfully!",
                        state="complete"
                    )
                else:
                    status.update(
                        label="❌ Failed",
                        state="error"
                    )

    if response:
        st.success("✨ Your notes are ready!")
        st.divider()
        st.markdown(response)
        st.divider()
        st.caption(f"⚡ Generated in {elapsed:.2f} seconds | Powered by Groq + Llama 3.3")
        st.download_button(
            label="Download Notes",
            data=response,
            file_name="summary_notes.txt",
            mime="text/plain",
            key="download_summary"
        )


# -------------------------
# Topic Page
# -------------------------
elif st.session_state.page == "topic":

    st.title("💡 Generate from Topic")

    topic = st.text_input(
        "Enter a topic"
    )

    user_instructions = st.text_area(
        "Additional Instructions (Optional)"
    )

    response = None

    col1, col2 = st.columns(2)

    with col1:
        back = st.button("⬅ Back", use_container_width=True)
    
    if back:
        st.session_state.page = "home"
        st.rerun()

    with col2:
        generate = st.button("Generate", use_container_width=True)

    if generate:
        st.divider()
        prompt = build_topic_prompt(topic, user_instructions)

        with st.status("🤖 AI is working...", expanded=True) as status:
            st.write("📝 Understanding your request...")
            
            success = False
            try:
                start = time.time()
                response = get_notes(prompt)
                elapsed = time.time() - start
                success = True

                st.write("🧠 Generating notes...")
                st.write("✨ Formatting the response...")
            
                st.caption(f"⚡ Generated in {elapsed:.2f} seconds")
            
            except groq.AuthenticationError as e:
                logging.error(f"Auth error: {e}")
                st.error(":gray[⚠️ Invalid API key. Check your .env file.]")

            except groq.RateLimitError as e:
                logging.error(f"Rate limit: {e}")
                st.error(":gray[⚠️ Too many requests — please wait a moment and try again.]")

            except groq.APIConnectionError as e:
                logging.error(f"Connection error: {e}")
                st.error(":gray[⚠️ Unable to connect. Check your internet.]")

            except Exception as e:
                logging.error(f"Unexpected error: {e}")
                st.error(":gray[⚠️ Something went wrong. Please try again.]")

            finally:
                if success:
                    status.update(
                        label="✅ Notes generated successfully!",
                        state="complete"
                    )
                else:
                    status.update(
                        label="❌ Failed",
                        state="error"
                    )

    if response:
        st.success("✨ Your notes are ready!")
        st.divider()
        st.markdown(response)
        st.divider()
        st.caption(f"⚡ Generated in {elapsed:.2f} seconds | Powered by Groq + Llama 3.3")
        st.download_button(
            label="Download Notes",
            data=response,
            file_name="topic_notes.txt",
            mime="text/plain",
            key="download_topic"
        )