#!/bin/bash

echo "========================================"
echo "Stock Learning Hub - Deployment Helper"
echo "========================================"
echo ""
echo "This will help you deploy the app with built-in user manual"
echo ""
echo "OPTION 1: Test Locally First (Recommended)"
echo "OPTION 2: Deploy to Streamlit Cloud"
echo "OPTION 3: Exit"
echo ""
read -p "Enter your choice (1, 2, or 3): " choice

case $choice in
    1)
        echo ""
        echo "========================================"
        echo "Testing Locally..."
        echo "========================================"
        echo ""
        echo "Starting Streamlit app..."
        echo "App will open at: http://localhost:8501"
        echo ""
        echo "To verify user manual:"
        echo "1. Wait for app to open"
        echo "2. Click 'User Manual' in left sidebar"
        echo "3. Check all 6 sections display"
        echo ""
        echo "Press Ctrl+C to stop the app"
        echo ""
        cd Stock-Learning-Hub
        streamlit run app.py
        ;;
    2)
        echo ""
        echo "========================================"
        echo "Deploy to Streamlit Cloud"
        echo "========================================"
        echo ""
        echo "STEP 1: Push to GitHub"
        echo "-----------------------"
        echo ""
        read -p "Enter your GitHub repo URL (e.g., https://github.com/username/repo.git): " repo
        echo ""
        echo "Initializing git..."
        git init
        echo ""
        echo "Adding all files..."
        git add .
        echo ""
        echo "Committing..."
        git commit -m "Stock Learning Hub with built-in user manual"
        echo ""
        echo "Adding remote..."
        git remote add origin "$repo"
        echo ""
        echo "Pushing to GitHub..."
        git branch -M main
        git push -u origin main
        echo ""
        echo "========================================"
        echo "STEP 2: Deploy on Streamlit Cloud"
        echo "========================================"
        echo ""
        echo "1. Go to: https://share.streamlit.io"
        echo "2. Sign in with GitHub"
        echo "3. Click 'New app'"
        echo "4. Fill in:"
        echo "   - Repository: your-username/stock-learning-hub"
        echo "   - Branch: main"
        echo "   - Main file path: Stock-Learning-Hub/app.py"
        echo "5. Click 'Deploy!'"
        echo ""
        echo "Your app will be live in 2-3 minutes!"
        echo ""
        echo "Opening Streamlit Cloud in browser..."
        if command -v xdg-open > /dev/null; then
            xdg-open https://share.streamlit.io
        elif command -v open > /dev/null; then
            open https://share.streamlit.io
        else
            echo "Please open: https://share.streamlit.io"
        fi
        echo ""
        read -p "Press Enter to continue..."
        ;;
    3)
        echo "Exiting..."
        exit 0
        ;;
    *)
        echo "Invalid choice. Exiting..."
        exit 1
        ;;
esac

echo ""
echo "========================================"
echo "Done!"
echo "========================================"
echo ""
echo "For help, see:"
echo "- DEPLOY_WITH_MANUAL.md (complete guide)"
echo "- DEPLOY_NOW.md (quick checklist)"
echo ""
