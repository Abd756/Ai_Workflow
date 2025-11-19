# 🎬 AI Video Workflow - Streamlit UI

A beautiful web interface for generating AI-powered video prompts using Streamlit.

## 🚀 Quick Start

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Set Up Environment
Create a `.env` file with your Google API key:
```
GOOGLE_API_KEY=your_gemini_api_key_here
```

### 3. Launch the App

**Method 1: Using the launcher script (Recommended)**
```bash
python launch_streamlit.py
```

**Method 2: Direct Streamlit command**
```bash
streamlit run streamlit_app.py
```

**Method 3: With custom configuration**
```bash
streamlit run streamlit_app.py --theme.primaryColor="#667eea" --theme.base="light"
```

## 📱 UI Features

### 🎯 **Current Features (Phase 1)**

#### **1. Beautiful Interface**
- Modern gradient design
- Responsive layout  
- Professional color scheme
- Interactive animations

#### **2. Smart Input System**
- Large text area for business descriptions
- Real-time word/character counting
- Input validation with helpful hints
- Example templates for different industries

#### **3. Loading Experience**
- Animated loading sequence
- Progressive status messages
- Visual progress indicators
- Professional waiting experience

#### **4. Attractive Prompt Display**
- Tab-based organization (Overview, Details, Export)
- Color-coded scene cards
- Expandable full prompt views
- Individual prompt statistics

#### **5. Export Options**
- Copy individual prompts to clipboard
- Download as JSON format
- Download as formatted text file
- Timestamped file naming

#### **6. Progress Tracking**
- Sidebar progress indicators
- Generation statistics
- Workflow step visualization
- Real-time status updates

## 🎨 **UI Layout & Design**

### **Main Header**
```
🎬 AI Video Workflow Studio
Transform your business description into professional video prompts using AI
```

### **Sidebar Navigation**
- Workflow progress tracker
- Step-by-step indicators  
- Prompt statistics
- Quick actions

### **Main Content Areas**

#### **Input Phase:**
- Business description text area
- Example templates expandable section
- Input validation indicators
- Generate prompts button

#### **Results Phase:**
- Success message with celebration
- Tabbed prompt display:
  - **📋 Scene Overview**: Card-based scene preview
  - **📊 Prompt Details**: Full expandable prompts
  - **💾 Export Options**: Download and copy features

## 🛠️ **Technical Features**

### **Session State Management**
```python
- prompts_generated: bool
- generated_prompts: VideoScenePrompts  
- user_input: str
- generation_timestamp: str
```

### **Custom CSS Styling**
- Gradient backgrounds
- Professional card layouts
- Responsive design
- Custom animations
- Modern color palette

### **Interactive Elements**
- Progress bars during generation
- Expandable sections
- Copy-to-clipboard functionality
- File download buttons
- Navigation tabs

## 🔄 **User Flow**

### **Step 1: Input**
```
User enters business description
↓
Real-time validation & hints
↓  
Click "Generate Video Prompts"
```

### **Step 2: Processing** 
```
Loading animation sequence:
🧠 Analyzing your business description...
🎯 Understanding your target audience...
🎨 Crafting creative scene concepts...
📝 Generating professional video prompts...
✨ Adding cinematic details...
🎬 Finalizing your video scenes...
```

### **Step 3: Results**
```
Success message displayed
↓
Attractive prompt cards shown
↓
Export and navigation options
```

## 📊 **Input Guidelines**

### **Recommended Input Structure:**
```
I run [Company Name], a [Industry] company.
We [Main Services/Products].

Target audience: [Who you serve]
Video goals: [What you want to achieve]

Specific scenes I'd like:
- [Scene 1 idea]
- [Scene 2 idea]  
- [Scene 3 idea]
- [Unique selling points]
```

### **Quality Indicators:**
- ✅ **50+ words**: Great detail level
- ⚠️ **25-49 words**: Add more details  
- ❌ **<25 words**: Need more information

## 🎯 **Example Inputs**

### **Restaurant:**
```
I run Green Garden Cafe, a sustainable farm-to-table restaurant in downtown. 
We source ingredients locally, offer organic dishes, and create a cozy atmosphere 
for families and professionals. I want videos showcasing our fresh ingredient 
preparation, happy customers, cozy atmosphere, and sustainability commitment.
```

### **Tech Company:**
```  
I run TechFlow Solutions, a software development company specializing in AI automation.
We help businesses streamline operations through intelligent automation and cloud solutions.
I want professional videos showing our modern office, team collaboration, AI solutions
in action, and client testimonials that convey innovation and expertise.
```

### **Real Estate:**
```
I run iCONNCT, a real estate technology platform that works like Uber for real estate.
We offer instant agent connections, video calls, and seamless property tours.
I want videos demonstrating our technology, showing agents helping clients,
property showcases, and satisfied customers.
```

## 🎨 **Customization Options**

### **Theme Colors**
```python
Primary: #667eea (Purple-blue gradient)
Secondary: #764ba2 (Deep purple)  
Background: #ffffff (Clean white)
Cards: #f5f7fa (Light gray-blue)
Success: #d4edda (Light green)
Warning: #fff3cd (Light yellow)
```

### **Layout Configuration**
```python
st.set_page_config(
    page_title="AI Video Workflow Studio",
    page_icon="🎬", 
    layout="wide",
    initial_sidebar_state="expanded"
)
```

## 🔜 **Coming Soon (Future Phases)**

### **Phase 2: Video Generation Integration**
- Connect to integrated_video_workflow.py
- Real-time video generation progress
- Interactive debugger UI
- Video preview capabilities

### **Phase 3: Video Management**
- Video gallery view
- Merge configuration UI  
- Download manager
- Batch processing interface

### **Phase 4: Advanced Features**
- User accounts & history
- Template library
- Custom prompt editing
- Analytics dashboard

## 🚨 **Troubleshooting**

### **Common Issues:**

#### **"Module not found" errors:**
```bash
pip install -r requirements.txt
```

#### **"GOOGLE_API_KEY not found":**
Create `.env` file:
```
GOOGLE_API_KEY=your_api_key_here
```

#### **App won't start:**
```bash
# Check if you're in the right directory
ls streamlit_app.py

# Try direct launch
python -m streamlit run streamlit_app.py
```

#### **Prompts not generating:**
- Check your Google API key
- Verify internet connection  
- Check API quota limits
- Try with shorter input first

### **Development Mode:**
```bash
# Auto-reload on file changes
streamlit run streamlit_app.py --server.runOnSave=true

# Debug mode
streamlit run streamlit_app.py --logger.level=debug
```

## 📁 **File Structure**
```
├── streamlit_app.py           # Main Streamlit application
├── launch_streamlit.py        # Easy launcher script
├── video_prompt_generator.py  # Backend prompt generation
├── requirements.txt           # Dependencies including Streamlit
└── .env                       # API keys (create this)
```

## 🎉 **Success Indicators**

When working properly, you should see:
- ✅ App loads at http://localhost:8501
- ✅ Input validation shows real-time feedback
- ✅ Generate button activates with sufficient input
- ✅ Loading animation plays during generation
- ✅ Four prompts display in attractive cards
- ✅ Export options work correctly

## 💡 **Tips for Best Experience**

1. **Use detailed business descriptions** (50+ words recommended)
2. **Include specific scene ideas** you want to see
3. **Mention your target audience** clearly
4. **Describe your unique selling points**
5. **Test with provided examples** first
6. **Save successful prompts** using export features

The Streamlit UI provides a professional, user-friendly interface for the AI video workflow, making it accessible to users without technical expertise! 🎬✨