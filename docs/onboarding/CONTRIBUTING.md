# 👋 Welcome to AI-AH!

Thank you for contributing to AI-AH! This guide will help you get started.

## 🚀 First Steps

1. **Read the Documentation**
   - [Project Context](../CONTEXT.md)
   - [Architecture](../ARCHITECTURE.md)
   - [Governance](../PROJECT_GOVERNANCE.md)

2. **Set Up Your Environment**
   ```bash
   # Clone the repository
   git clone https://github.com/your-org/ai-ah.git
   cd ai-ah
   
   # Set up Python environment
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   
   # Install dependencies
   pip install -r requirements-dev.txt
   pre-commit install
   ```

3. **Take the Tour**
   - Explore the codebase structure
   - Run the test suite: `pytest`
   - Start a local development server: `python -m ai_ah.main`

## 🛠 Development Workflow

1. **Before You Start**
   - Check open issues for tasks
   - Discuss significant changes in an issue first
   - For major changes, create an ADR (Architecture Decision Record)

2. **Making Changes**
   ```bash
   # Create a new branch
   git checkout -b feature/your-feature-name
   
   # Make your changes
   # Run tests and checks
   pre-commit run --all-files
   pytest
   
   # Commit with a descriptive message
   git commit -m "feat: add your feature"
   
   # Push and create a pull request
   git push -u origin feature/your-feature-name
   ```

3. **Code Review**
   - All changes require at least one approval
   - Address all review comments
   - Update documentation as needed

## 📚 Learning Resources

- [Terraform Documentation](https://www.terraform.io/docs/)
- [Kubernetes Documentation](https://kubernetes.io/docs/home/)
- [Python Best Practices](https://docs.python-guide.org/)

## 🆘 Need Help?

- Check the [FAQ](./FAQ.md)
- Open a [GitHub Issue](https://github.com/your-org/ai-ah/issues)
- Join our [Slack/Discord] channel

## 🙏 Thank You!

Your contributions help make AI-AH better for everyone!
