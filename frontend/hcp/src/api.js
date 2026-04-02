import axios from 'axios';

const API_URL = "http://127.0.0.1:8000";

export const chatWithAgent = async (message) => {
  try {
    const response = await axios.post(`${API_URL}/chat`, {
      message: message
    });
    return response.data;
  } catch (error) {
    console.error("Error chatting with agent:", error);
    throw error;
  }
};