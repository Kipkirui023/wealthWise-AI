"""
WealthWise AI - Main Application
Streamlit-based web interface for financial health assessment
"""

import streamlit as st
import pandas as pd
from inference_engine import WealthWiseInferenceEngine

# Page configuration
st.set_page_config(
    page_title="WealthWise AI",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="expanded"
)

def main():
    # Custom CSS for better styling
    st.markdown("""
    <style>
    .main-header {
        font-size: 2.5rem;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .score-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 10px;
        text-align: center;
        margin: 0.5rem;
    }
    .critical { color: #ff4b4b; font-weight: bold; }
    .high { color: #ff6b6b; }
    .medium { color: #ffa726; }
    .good { color: #66bb6a; }
    .excellent { color: #2e7d32; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)
    
    # Header
    st.markdown('<h1 class="main-header">💰 WealthWise AI</h1>', unsafe_allow_html=True)
    st.markdown("### Your Personal Financial Health Assessment System")
    
    # Sidebar for user input
    with st.sidebar:
        st.header("📊 Your Financial Profile")
        
        # Personal Information
        st.subheader("Personal Info")
        age = st.slider("Age", 18, 65, 25)
        
        # Income & Expenses
        st.subheader("Income & Expenses")
        monthly_income = st.number_input("Monthly Income ($)", min_value=0, value=5000, step=100)
        monthly_expenses = st.number_input("Monthly Expenses ($)", min_value=0, value=3500, step=100)
        housing_cost = st.number_input("Monthly Housing Cost ($)", min_value=0, value=1500, step=100)
        
        # Savings & Debt
        st.subheader("Savings & Debt")
        emergency_savings = st.number_input("Emergency Savings ($)", min_value=0, value=5000, step=500)
        retirement_savings = st.number_input("Retirement Savings ($)", min_value=0, value=15000, step=1000)
        monthly_savings = st.number_input("Monthly Savings ($)", min_value=0, value=500, step=50)
        total_monthly_debt = st.number_input("Monthly Debt Payments ($)", min_value=0, value=800, step=50)
        
        # Assessment button
        analyze_button = st.button("🚀 Analyze My Financial Health", type="primary", use_container_width=True)
    
    # Main content area
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("### How It Works")
        st.markdown("""
        WealthWise AI analyzes your financial data using expert financial rules to provide:
        - **Comprehensive Financial Health Score**
        - **Personalized Recommendations**
        - **Actionable Insights**
        - **Transparent Explanations**
        
        *All analysis is based on established financial planning principles and is for educational purposes.*
        """)
    
    with col2:
        st.markdown("### 💡 Tips for Accurate Results")
        st.markdown("""
        - Use accurate, recent numbers
        - Include all regular expenses
        - Count all debt payments
        - Be honest about savings
        """)
    
    # Process analysis when button is clicked
    if analyze_button:
        with st.spinner("Analyzing your financial health..."):
            # Prepare user data
            user_data = {
                'age': age,
                'monthly_income': monthly_income,
                'monthly_expenses': monthly_expenses,
                'housing_cost': housing_cost,
                'emergency_savings': emergency_savings,
                'retirement_savings': retirement_savings,
                'monthly_savings': monthly_savings,
                'total_monthly_debt': total_monthly_debt
            }
            
            # Initialize and run inference engine
            engine = WealthWiseInferenceEngine()
            results = engine.evaluate_financial_health(user_data)
            
            # Display results - PASS THE ENGINE TO THE FUNCTION
            display_results(results, user_data, engine)

def display_results(results, user_data, engine):
    """Display the analysis results in an organized way"""
    
    # Score and Grade Display
    st.markdown("---")
    st.markdown("## 📈 Your Financial Health Report")
    
    # Create columns for score cards
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        score_color = get_score_color(results['final_score'])
        st.markdown(f"""
        <div class="score-card">
            <h3>Overall Score</h3>
            <h2 style="color: {score_color};">{results['final_score']}/100</h2>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        grade_color = get_grade_color(results['grade'])
        st.markdown(f"""
        <div class="score-card">
            <h3>Grade</h3>
            <h2 style="color: {grade_color};">{results['grade']}</h2>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        priority_count = len([r for r in results['recommendations'] if r['severity'] in ['critical', 'high']])
        st.markdown(f"""
        <div class="score-card">
            <h3>Priority Actions</h3>
            <h2>{priority_count}</h2>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        total_recs = len(results['recommendations'])
        st.markdown(f"""
        <div class="score-card">
            <h3>Total Recommendations</h3>
            <h2>{total_recs}</h2>
        </div>
        """, unsafe_allow_html=True)
    
    # Progress bar for visual score representation
    st.progress(results['final_score'] / 100)
    st.caption(f"Financial Health Progress: {results['final_score']}%")
    
    # Financial Metrics Overview
    st.markdown("### 📊 Key Financial Metrics")
    metrics_col1, metrics_col2, metrics_col3, metrics_col4 = st.columns(4)
    
    with metrics_col1:
        debt_ratio = results['metrics']['debt_ratio']
        status = "✅ Good" if debt_ratio <= 0.36 else "⚠️ High"
        st.metric("Debt-to-Income Ratio", f"{debt_ratio:.1%}", status)
    
    with metrics_col2:
        savings_rate = results['metrics']['savings_rate']
        status = "✅ Good" if savings_rate >= 0.10 else "⚠️ Low"
        st.metric("Savings Rate", f"{savings_rate:.1%}", status)
    
    with metrics_col3:
        housing_ratio = results['metrics']['housing_ratio']
        status = "✅ Good" if housing_ratio <= 0.30 else "⚠️ High"
        st.metric("Housing Cost %", f"{housing_ratio:.1%}", status)
    
    with metrics_col4:
        coverage = results['metrics']['coverage_months']
        status = "✅ Good" if coverage >= 3 else "⚠️ Low"
        st.metric("Emergency Fund", f"{coverage:.1f} months", status)
    
    # Recommendations by Priority
    st.markdown("### 🎯 Personalized Recommendations")
    
    # Sort recommendations by priority - NOW engine is available
    sorted_recommendations = engine.get_recommendations_by_priority()
    
    # Display by severity categories
    critical_high = [r for r in sorted_recommendations if r['severity'] in ['critical', 'high']]
    medium = [r for r in sorted_recommendations if r['severity'] == 'medium']
    good_excellent = [r for r in sorted_recommendations if r['severity'] in ['good', 'excellent']]
    
    if critical_high:
        st.markdown("#### 🚨 Priority Actions (Critical/High)")
        for rec in critical_high:
            with st.expander(f"🔴 {rec['message']}", expanded=True):
                st.write(rec['explanation'])
                st.caption(f"Impact: {rec['score_impact']:+.1f} points")
    
    if medium:
        st.markdown("#### ⚠️ Areas for Improvement (Medium)")
        for rec in medium:
            with st.expander(f"🟡 {rec['message']}"):
                st.write(rec['explanation'])
                st.caption(f"Impact: {rec['score_impact']:+.1f} points")
    
    if good_excellent:
        st.markdown("#### ✅ What You're Doing Right (Good/Excellent)")
        for rec in good_excellent:
            with st.expander(f"🟢 {rec['message']}"):
                st.write(rec['explanation'])
                st.caption(f"Impact: {rec['score_impact']:+.1f} points")
    
    # Detailed Financial Analysis
    st.markdown("### 📋 Detailed Financial Analysis")
    
    # Create a summary table
    analysis_data = []
    for rec in sorted_recommendations:
        analysis_data.append({
            'Category': rec['category'].replace('_', ' ').title(),
            'Recommendation': rec['message'],
            'Severity': rec['severity'].title(),
            'Score Impact': f"{rec['score_impact']:+.1f}"
        })
    
    if analysis_data:
        st.table(pd.DataFrame(analysis_data))
    else:
        st.info("No specific recommendations generated. Your financial health appears to be excellent across all categories!")

def get_score_color(score):
    """Return color based on score"""
    if score >= 80: return "#2e7d32"  # Green
    elif score >= 60: return "#ffa726"  # Orange
    else: return "#ef5350"  # Red

def get_grade_color(grade):
    """Return color based on grade"""
    if grade in ['A+', 'A', 'A-']: return "#2e7d32"
    elif grade in ['B+', 'B', 'B-']: return "#ffa726"
    else: return "#ef5350"

if __name__ == "__main__":
    main()