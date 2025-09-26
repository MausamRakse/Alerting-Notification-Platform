#!/usr/bin/env python3
"""
Alerting & Notification Platform
Main application entry point
"""

import os
import sys
from app import create_app

# Add the project directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def main():
    """Main entry point for the application."""
    # Get configuration from environment
    config_name = os.getenv('FLASK_ENV', 'development')
    
    # Create and configure the Flask app
    app = create_app(config_name)
    
    # Get host and port from environment
    host = os.getenv('HOST', '127.0.0.1')
    port = int(os.getenv('PORT', 5000))
    debug = config_name == 'development'
    
    print(f"\n🚀 Starting Alerting & Notification Platform")
    print(f"📍 Running on http://{host}:{port}")
    print(f"🔧 Environment: {config_name}")
    print(f"🐛 Debug mode: {debug}")
    
    if config_name == 'development':
        print(f"\n📚 API Documentation:")
        print(f"   Admin APIs: http://{host}:{port}/api/admin/")
        print(f"   User APIs:  http://{host}:{port}/api/user/")
        print(f"   Analytics:  http://{host}:{port}/api/analytics/")
        print(f"\n💡 Sample admin user: admin@example.com")
    
    print(f"\n" + "="*50)
    
    # Run the application
    try:
        app.run(host=host, port=port, debug=debug)
    except KeyboardInterrupt:
        print(f"\n👋 Shutting down Alerting Platform...")
    except Exception as e:
        print(f"\n❌ Error starting application: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main() 