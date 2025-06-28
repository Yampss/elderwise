# ElderWise Deployment Guide

## Quick Start (Local Development)

### Prerequisites
- Python 3.9+ (3.11 recommended)
- Anaconda or Miniconda
- Google Gemini API key (free at [Google AI Studio](https://makersuite.google.com/app/apikey))

### 1-Minute Setup
```bash
git clone https://github.com/yourusername/elderwise.git
cd elderwise
conda create -n elderwise python=3.11 -y
conda activate elderwise
pip install -r requirements.txt
streamlit run app.py
```

## Detailed Setup

### Step 1: Environment Setup
```bash
# Create conda environment
conda create -n elderwise python=3.11 -y
conda activate elderwise

# Or use the automated script
./setup_env.sh  # Linux/Mac
setup_env.bat   # Windows
```

### Step 2: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 3: Configuration
```bash
# Copy environment template
cp .env.example .env

# Edit with your API key
nano .env  # or use your preferred editor
```

### Step 4: Run Application
```bash
# Start the application
streamlit run app.py

# Or use the run scripts
./run.sh  # Linux/Mac
run.bat   # Windows
```

## Production Deployment

### Docker Deployment

1. **Build Docker Image**
```bash
docker build -t elderwise:latest .
```

2. **Run Container**
```bash
docker run -p 8501:8501 \
  -e GEMINI_API_KEY=your_api_key \
  -v elderwise_data:/app/data \
  elderwise:latest
```

### Cloud Deployment Options

#### Streamlit Cloud
1. Fork this repository
2. Connect to Streamlit Cloud
3. Add `GEMINI_API_KEY` to secrets
4. Deploy with one click

#### Heroku
```bash
heroku create your-elderwise-app
heroku config:set GEMINI_API_KEY=your_api_key
git push heroku main
```

#### Railway
1. Connect GitHub repository
2. Add environment variables
3. Deploy automatically

#### Google Cloud Run
```bash
# Build and deploy
gcloud run deploy elderwise \
  --source . \
  --platform managed \
  --region us-central1 \
  --set-env-vars GEMINI_API_KEY=your_api_key
```

### Self-Hosted Server

#### Using systemd (Linux)
```ini
[Unit]
Description=ElderWise Application
After=network.target

[Service]
Type=simple
User=elderwise
WorkingDirectory=/opt/elderwise
Environment=PATH=/opt/elderwise/venv/bin
ExecStart=/opt/elderwise/venv/bin/streamlit run app.py --server.port 8501
Restart=always

[Install]
WantedBy=multi-user.target
```

#### Using nginx reverse proxy
```nginx
server {
    listen 80;
    server_name your-domain.com;
    
    location / {
        proxy_pass http://localhost:8501;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host $host;
        proxy_cache_bypass $http_upgrade;
    }
}
```

## Environment Variables

| Variable | Description | Default | Required |
|----------|-------------|---------|----------|
| `GEMINI_API_KEY` | Google Gemini API key | None | Yes |
| `ELDERWISE_DEBUG` | Enable debug mode | false | No |
| `ELDERWISE_DATA_DIR` | Data storage directory | ./data | No |
| `ELDERWISE_MAX_UPLOAD_SIZE_MB` | Max file upload size | 50 | No |

## Security Considerations

### API Key Security
- Never commit API keys to version control
- Use environment variables or secrets management
- Rotate keys regularly
- Monitor API usage

### Data Protection
- Enable HTTPS in production
- Implement user authentication if needed
- Regular data backups
- Comply with privacy regulations

### Content Moderation
- Enable AI content filtering
- Implement user reporting system
- Regular content audits
- Community guidelines enforcement

## Monitoring and Maintenance

### Health Checks
```bash
# Application health
curl http://localhost:8501/_stcore/health

# API connectivity
python -c "from src.ai_engine import AIEngine; print(AIEngine().is_ready())"
```

### Log Monitoring
- Monitor Streamlit logs for errors
- Track API usage and limits
- Monitor storage usage
- User activity analytics

### Backup Strategy
```bash
# Backup user data
tar -czf elderwise_backup_$(date +%Y%m%d).tar.gz data/

# Database backup (if using database)
pg_dump elderwise > elderwise_backup_$(date +%Y%m%d).sql
```

## Troubleshooting

### Common Issues

1. **Import Errors**
   ```bash
   # Check environment
   conda list
   pip list
   which python
   ```

2. **API Key Issues**
   ```bash
   # Test API key
   python -c "import os; print('API Key:', os.getenv('GEMINI_API_KEY', 'Not set'))"
   ```

3. **Port Conflicts**
   ```bash
   # Use different port
   streamlit run app.py --server.port 8502
   ```

4. **Storage Issues**
   ```bash
   # Check disk space
   df -h
   # Check permissions
   ls -la data/
   ```

### Performance Optimization

1. **Caching Configuration**
   ```python
   # In .streamlit/config.toml
   [server]
   maxUploadSize = 50
   
   [theme]
   base = "light"
   ```

2. **Resource Limits**
   - Monitor memory usage
   - Limit concurrent users
   - Implement request rate limiting
   - Optimize file storage

## Scaling Considerations

### Horizontal Scaling
- Load balancer configuration
- Shared storage setup
- Session state management
- Database migration

### Performance Monitoring
- Response time tracking
- Error rate monitoring
- Resource utilization
- User experience metrics

## Support and Updates

### Getting Help
- Check the [Issues](https://github.com/yourusername/elderwise/issues) page
- Review [Documentation](DOCUMENTATION.md)
- Join community discussions
- Contact maintainers

### Updating
```bash
# Pull latest changes
git pull origin main

# Update dependencies
pip install -r requirements.txt --upgrade

# Restart application
systemctl restart elderwise  # for systemd
```

### Contributing
See [CONTRIBUTING.md](CONTRIBUTING.md) for development setup and contribution guidelines.
