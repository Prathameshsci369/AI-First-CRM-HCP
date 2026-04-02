import React, { useState } from 'react';
import { useSelector, useDispatch } from 'react-redux';
import { addMessage, updateForm } from './hcpSlice';
import { chatWithAgent } from './api';

function App() {
  const dispatch = useDispatch();
  const { chatHistory, form } = useSelector((state) => state.hcp);
  const [input, setInput] = useState("");

  // --- Color Palette (Professional CRM) ---
  const colors = {
    primary: '#0F3A7D',      // Deep Blue
    secondary: '#7C3AED',    // Vibrant Purple
    accent: '#06B6D4',       // Teal
    darkBg: '#0F172A',
    lightBg: '#F0F9FF',
    white: '#FFFFFF',
  };

  // --- Styles Configuration ---
  const styles = {
    page: {
      display: 'flex',
      height: '100vh',
      backgroundColor: colors.lightBg,
      fontFamily: 'Inter, system-ui, sans-serif',
      color: colors.primary,
    },
    // RIGHT PANEL: CHAT
    chatPanel: {
      width: '420px',
      backgroundColor: colors.white,
      borderLeft: `3px solid ${colors.accent}`,
      display: 'flex',
      flexDirection: 'column',
      boxShadow: '-8px 0 32px rgba(15, 58, 125, 0.15)',
      zIndex: 10,
      order: 2,
    },
    chatHeader: {
      padding: '24px',
      background: `linear-gradient(135deg, ${colors.primary} 0%, ${colors.secondary} 100%)`,
      fontSize: '18px',
      fontWeight: '700',
      color: colors.white,
      display: 'flex',
      alignItems: 'center',
      gap: '12px',
      borderRadius: '0 0 0 12px',
    },
    chatMessages: {
      flex: 1,
      padding: '20px',
      overflowY: 'auto',
      backgroundColor: '#F8FAFC',
      display: 'flex',
      flexDirection: 'column',
      gap: '14px',
    },
    chatInputArea: {
      padding: '20px',
      borderTop: `1px solid ${colors.accent}`,
      backgroundColor: colors.white,
      borderRadius: '0 0 0 12px',
    },
    messageBubble: (role) => ({
      maxWidth: '85%',
      padding: '12px 16px',
      borderRadius: '14px',
      fontSize: '14px',
      lineHeight: '1.5',
      alignSelf: role === 'user' ? 'flex-end' : 'flex-start',
      backgroundColor: role === 'user' ? colors.primary : colors.lightBg,
      color: role === 'user' ? colors.white : colors.primary,
      border: role === 'user' ? 'none' : `2px solid ${colors.accent}`,
      boxShadow: role === 'user' ? `0 4px 12px rgba(15, 58, 125, 0.2)` : 'none',
    }),
    inputField: {
      width: '100%',
      padding: '12px 16px',
      borderRadius: '10px',
      border: `2px solid ${colors.accent}`,
      outline: 'none',
      transition: 'all 0.3s',
      fontSize: '14px',
      backgroundColor: colors.white,
      color: colors.primary,
      fontFamily: 'inherit',
    },
    sendButton: {
      backgroundColor: colors.secondary,
      color: colors.white,
      border: 'none',
      padding: '12px 24px',
      borderRadius: '10px',
      fontWeight: '600',
      cursor: 'pointer',
      marginLeft: '10px',
      transition: 'all 0.3s',
      boxShadow: `0 4px 12px rgba(124, 58, 237, 0.3)`,
    },

    // LEFT PANEL: FORM
    formPanel: {
      flex: 1,
      padding: '40px',
      overflowY: 'auto',
      display: 'flex',
      justifyContent: 'center',
      background: `linear-gradient(135deg, ${colors.lightBg} 0%, #E0F2FE 100%)`,
      order: 1,
    },
    formCard: {
      backgroundColor: colors.white,
      padding: '40px',
      borderRadius: '20px',
      boxShadow: '0 20px 40px rgba(15, 58, 125, 0.15)',
      width: '100%',
      maxWidth: '900px',
      border: `2px solid ${colors.accent}`,
    },
    formHeader: {
      marginBottom: '32px',
      borderBottom: `3px solid ${colors.accent}`,
      paddingBottom: '16px',
    },
    formTitle: {
      fontSize: '28px',
      fontWeight: '700',
      background: `linear-gradient(135deg, ${colors.primary} 0%, ${colors.secondary} 100%)`,
      WebkitBackgroundClip: 'text',
      WebkitTextFillColor: 'transparent',
      margin: 0,
    },
    formSubtitle: {
      fontSize: '14px',
      color: colors.accent,
      marginTop: '8px',
      fontWeight: '500',
    },
    formGrid: {
      display: 'grid',
      gridTemplateColumns: '1fr 1fr',
      gap: '24px',
    },
    label: {
      display: 'block',
      fontSize: '13px',
      fontWeight: '700',
      color: colors.primary,
      marginBottom: '8px',
      textTransform: 'uppercase',
      letterSpacing: '0.1em',
    },
    // Custom Radio Buttons for Sentiment
    sentimentGroup: {
      display: 'flex',
      gap: '12px',
      marginTop: '10px',
    },
    sentimentOption: (value, current) => ({
      flex: 1,
      padding: '12px',
      borderRadius: '10px',
      border: `2px solid ${current === value ? colors.secondary : colors.accent}`,
      textAlign: 'center',
      cursor: 'pointer',
      fontSize: '14px',
      fontWeight: '600',
      backgroundColor: current === value ? 
        (value === 'Positive' ? `${colors.secondary}15` : value === 'Negative' ? '#FEE2E215' : `${colors.accent}15`) 
        : colors.white,
      color: current === value ? 
        (value === 'Positive' ? colors.secondary : value === 'Negative' ? '#DC2626' : colors.accent) 
        : colors.accent,
      transition: 'all 0.3s',
      boxShadow: current === value ? `0 4px 12px ${current === value ? colors.secondary : colors.accent}30` : 'none',
    }),
    saveButton: {
      background: `linear-gradient(135deg, ${colors.secondary} 0%, ${colors.accent} 100%)`,
      color: colors.white,
      border: 'none',
      padding: '14px 32px',
      borderRadius: '10px',
      fontWeight: '700',
      fontSize: '16px',
      cursor: 'pointer',
      marginTop: '20px',
      float: 'right',
      boxShadow: `0 8px 20px rgba(124, 58, 237, 0.3)`,
      transition: 'all 0.3s',
    }
  };

  // --- Logic ---
  const handleSend = async () => {
    console.log("⏱️  [INIT] handleSend triggered");
    
    if (!input.trim()) {
      console.warn("⚠️  [VALIDATION] Empty input detected, aborting");
      return;
    }

    console.log("📤 [USER INPUT] Message:", input);
    console.log("📊 [STATE] Current form state:", form);
    
    dispatch(addMessage({ role: 'user', content: input }));
    const userMsg = input;
    setInput(""); 
    console.log("✅ [DISPATCH] User message added to chat history");

    try {
      console.log("🔄 [API] Sending request to chatWithAgent...");
      const startTime = performance.now();
      
      const response = await chatWithAgent(userMsg);
      
      const endTime = performance.now();
      console.log(`⏱️  [API] Response time: ${(endTime - startTime).toFixed(2)}ms`);
      
      console.log("📥 [BACKEND RESPONSE] Full response object:", response);
      console.log("💬 [RESPONSE] Assistant message:", response.response);
      console.log("🔧 [TOOLS] Tools called:", response.tool_calls);
      
      dispatch(addMessage({ role: 'assistant', content: response.response }));
      console.log("✅ [DISPATCH] Assistant message added to chat history");

      if (response.tool_calls && response.tool_calls.length > 0) {
        console.log(`🧩 [TOOL CALLS] Found ${response.tool_calls.length} tool call(s)`);
        
        const args = response.tool_calls[0].args;
        console.log("🔍 [TOOL ARGS] Extracted arguments:", args);
        console.log("🔍 [TOOL NAME] Tool used:", response.tool_calls[0].name);
        
        const formUpdate = {
          hcp_name: args.hcp_name || form.hcp_name,
          interaction_type: args.interaction_type || form.interaction_type,
          topics_discussed: args.topics_discussed || form.topics_discussed,
          hcp_sentiment: args.hcp_sentiment || form.hcp_sentiment,
          outcome_next_steps: args.outcome_next_steps || form.outcome_next_steps,
        };
        
        console.log("📋 [FORM UPDATE] Prepared form update:", formUpdate);
        console.log("🔄 [FORM DIFF] Old values:", {
          hcp_name: form.hcp_name,
          interaction_type: form.interaction_type,
          topics_discussed: form.topics_discussed,
          hcp_sentiment: form.hcp_sentiment,
          outcome_next_steps: form.outcome_next_steps,
        });
        
        dispatch(updateForm(formUpdate));
        console.log("✅ [DISPATCH] Form updated with AI-extracted data");
      } else {
        console.log("ℹ️  [NO TOOLS] No tool calls in response");
      }
      
      console.log("✨ [SUCCESS] handleSend completed successfully");

    } catch (error) {
      console.error("❌ [ERROR] Exception caught:", error);
      console.error("❌ [ERROR] Error type:", error.constructor.name);
      console.error("❌ [ERROR] Stack trace:", error.stack);
      
      dispatch(addMessage({ role: 'assistant', content: "Error connecting to server." }));
      console.log("✅ [DISPATCH] Error message added to chat history");
    }
  };

  const handleChange = (e) => {
    dispatch(updateForm({ [e.target.name]: e.target.value }));
  };

  return (
    <div style={styles.page}>
      
      {/* LEFT: LOG INTERACTION FORM */}
      <div style={styles.formPanel}>
        <div style={styles.formCard}>
          <div style={styles.formHeader}>
            <h2 style={styles.formTitle}>Log HCP Interaction</h2>
            <p style={styles.formSubtitle}>Auto-filled by AI or edit manually below.</p>
          </div>

          <div style={styles.formGrid}>
            
            {/* HCP Name (Full Width) */}
            <div style={{ gridColumn: 'span 2' }}>
              <label style={styles.label}>🏥 HCP Name</label>
              <input 
                name="hcp_name" 
                value={form.hcp_name} 
                onChange={handleChange} 
                placeholder="Dr. Full Name"
                style={styles.inputField}
                onFocus={(e) => e.target.style.borderColor = colors.secondary}
                onBlur={(e) => e.target.style.borderColor = colors.accent}
              />
            </div>

            {/* Type */}
            <div>
              <label style={styles.label}>📋 Type</label>
              <select 
                name="interaction_type" 
                value={form.interaction_type} 
                onChange={handleChange}
                style={{...styles.inputField, cursor: 'pointer'}}
                onFocus={(e) => e.target.style.borderColor = colors.secondary}
                onBlur={(e) => e.target.style.borderColor = colors.accent}
              >
                <option>Meeting</option>
                <option>Call</option>
                <option>Sample Request</option>
                <option>Email</option>
              </select>
            </div>

            {/* Date */}
            <div>
              <label style={styles.label}>📅 Date</label>
              <input 
                type="date" 
                name="interaction_date" 
                value={form.interaction_date} 
                onChange={handleChange} 
                style={styles.inputField}
                onFocus={(e) => e.target.style.borderColor = colors.secondary}
                onBlur={(e) => e.target.style.borderColor = colors.accent}
              />
            </div>

            {/* Topics (Full Width) */}
            <div style={{ gridColumn: 'span 2' }}>
              <label style={styles.label}>💭 Topics Discussed</label>
              <textarea 
                name="topics_discussed" 
                value={form.topics_discussed} 
                onChange={handleChange} 
                rows="3"
                placeholder="Summary of discussion..."
                style={styles.inputField}
                onFocus={(e) => e.target.style.borderColor = colors.secondary}
                onBlur={(e) => e.target.style.borderColor = colors.accent}
              />
            </div>

            {/* Sentiment Selector (Custom UI) */}
            <div style={{ gridColumn: 'span 2' }}>
              <label style={styles.label}>😊 HCP Sentiment</label>
              <div style={styles.sentimentGroup}>
                {['Positive', 'Neutral', 'Negative'].map(s => (
                  <div 
                    key={s} 
                    style={styles.sentimentOption(s, form.hcp_sentiment)}
                    onClick={() => dispatch(updateForm({ hcp_sentiment: s }))}
                  >
                    {s === 'Positive' ? '😊' : s === 'Negative' ? '😞' : '😐'} {s}
                  </div>
                ))}
              </div>
            </div>

            {/* Outcome (Full Width) */}
            <div style={{ gridColumn: 'span 2' }}>
              <label style={styles.label}>🎯 Outcome / Next Steps</label>
              <textarea 
                name="outcome_next_steps" 
                value={form.outcome_next_steps} 
                onChange={handleChange} 
                rows="3"
                placeholder="Follow-up actions..."
                style={styles.inputField}
                onFocus={(e) => e.target.style.borderColor = colors.secondary}
                onBlur={(e) => e.target.style.borderColor = colors.accent}
              />
            </div>

          </div>
          
          <div style={{ overflow: 'hidden' }}> {/* Clearfix for float button */}
            <button 
              style={styles.saveButton}
              onMouseOver={(e) => {
                e.target.style.transform = 'translateY(-3px)';
                e.target.style.boxShadow = `0 12px 28px rgba(124, 58, 237, 0.4)`;
              }}
              onMouseOut={(e) => {
                e.target.style.transform = 'translateY(0)';
                e.target.style.boxShadow = `0 8px 20px rgba(124, 58, 237, 0.3)`;
              }}
            >
              💾 Save Interaction
            </button>
          </div>
        </div>
      </div>

      {/* RIGHT: CHAT INTERFACE */}
      <div style={styles.chatPanel}>
        <div style={styles.chatHeader}>
          <span style={{ fontSize: '20px' }}>🤖</span> <span style={{ letterSpacing: '0.5px' }}>AI CRM Assistant</span>
        </div>

        <div style={styles.chatMessages}>
          {chatHistory.map((msg, index) => (
            <div key={index} style={styles.messageBubble(msg.role)}>
              {msg.content}
            </div>
          ))}
        </div>

        <div style={styles.chatInputArea}>
          <div style={{ display: 'flex', gap: '8px' }}>
            <input 
              type="text" 
              value={input} 
              onChange={(e) => setInput(e.target.value)}
              onKeyPress={(e) => e.key === 'Enter' && handleSend()}
              placeholder="e.g., Log meeting with Dr. Smith..." 
              style={styles.inputField}
              onFocus={(e) => e.target.style.borderColor = colors.secondary}
              onBlur={(e) => e.target.style.borderColor = colors.accent}
            />
            <button 
              onClick={handleSend} 
              style={styles.sendButton}
              onMouseOver={(e) => {
                e.target.style.backgroundColor = colors.accent;
                e.target.style.transform = 'translateY(-2px)';
              }}
              onMouseOut={(e) => {
                e.target.style.background = `linear-gradient(135deg, ${colors.secondary} 0%, ${colors.accent} 100%)`;
                e.target.style.transform = 'translateY(0)';
              }}
            >
              Send
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}

export default App;