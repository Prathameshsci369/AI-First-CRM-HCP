import { createSlice } from '@reduxjs/toolkit';

const initialState = {
  chatHistory: [], // Stores the conversation
  form: {
    hcp_name: "",
    interaction_type: "Meeting",
    interaction_date: "",
    interaction_time: "",
    attendees: "",
    topics_discussed: "",
    voice_note_summary: "",
    voice_note_consent: false,
    shared_materials: "",
    hcp_sentiment: "Neutral",
    outcome_next_steps: ""
  }
};

export const hcpSlice = createSlice({
  name: 'hcp',
  initialState,
  reducers: {
    addMessage: (state, action) => {
      state.chatHistory.push(action.payload);
    },
    updateForm: (state, action) => {
      // Merge the AI data into the form
      state.form = { ...state.form, ...action.payload };
    },
    resetForm: (state) => {
      state.form = initialState.form;
    }
  },
});

export const { addMessage, updateForm, resetForm } = hcpSlice.actions;
export default hcpSlice.reducer;