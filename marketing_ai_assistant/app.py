import streamlit as st
import uuid
from rag import rag
import db


def handle_question(question):
    # Generate a unique conversation ID
    conversation_id = str(uuid.uuid4())

    # Get the answer from the rag function
    answer_data = rag(question)

    # Save the conversation to the database
    db.save_conversation(
        conversation_id=conversation_id,
        question=question,
        answer_data=answer_data,
    )

    # Return the answer and the conversation ID (ID is not shown to the user)
    return {
        "conversation_id": conversation_id,
        "answer": answer_data["answer"],
    }


def handle_feedback(conversation_id, feedback_value):
    # Save feedback to the database
    db.save_feedback(
        conversation_id=conversation_id,
        feedback=feedback_value,
    )
    # Return feedback received message
    return "Feedback received"


# Streamlit app
def main():
    st.title("MARI - Marketing AI Assistant")

    # Input for the user's question
    question = st.text_input("Ask a question", "")

    # Display previous conversation if any
    if "conversation_id" in st.session_state:
        st.markdown(f"**Answer:** {st.session_state.get('answer', '')}")
        feedback_value = st.radio("Feedback", ["+1", "-1"], key="feedback_radio")
        if st.button("Submit Feedback"):
            feedback_status = handle_feedback(
                st.session_state["conversation_id"], feedback_value
            )
            st.success(feedback_status)
            # Clear conversation state after feedback submission
            st.session_state.pop("conversation_id", None)
            st.session_state.pop("answer", None)
            st.session_state.pop("feedback_radio", None)
    else:
        if st.button("Submit"):
            if question:
                result = handle_question(question)
                answer = result["answer"]
                conversation_id = result["conversation_id"]

                # Show answer
                st.session_state["conversation_id"] = conversation_id
                st.session_state["answer"] = answer

                # Show feedback section
                st.markdown(f"**Answer:** {answer}")
                st.radio("Feedback", ["+1", "-1"], key="feedback_radio")
                if st.button("Submit Feedback"):
                    feedback_value = st.session_state["feedback_radio"]
                    feedback_status = handle_feedback(conversation_id, feedback_value)
                    st.success(feedback_status)
                    # Clear conversation state after feedback submission
                    st.session_state.pop("conversation_id", None)
                    st.session_state.pop("answer", None)
                    st.session_state.pop("feedback_radio", None)
            else:
                st.warning("Please enter a question before submitting.")


if __name__ == "__main__":
    main()