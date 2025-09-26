#!/usr/bin/env python3
"""
System Test Script for Alerting & Notification Platform
Tests basic functionality to ensure the system is working correctly.
"""

import requests
import json
import time
from datetime import datetime, timedelta

BASE_URL = 'http://127.0.0.1:5000'

def test_api_endpoint(method, endpoint, data=None, expected_status=200):
    """Test an API endpoint and return the response."""
    url = f"{BASE_URL}{endpoint}"
    
    try:
        if method.upper() == 'GET':
            response = requests.get(url)
        elif method.upper() == 'POST':
            response = requests.post(url, json=data, headers={'Content-Type': 'application/json'})
        elif method.upper() == 'PUT':
            response = requests.put(url, json=data, headers={'Content-Type': 'application/json'})
        else:
            raise ValueError(f"Unsupported method: {method}")
        
        print(f"{'✅' if response.status_code == expected_status else '❌'} {method} {endpoint} - Status: {response.status_code}")
        
        if response.status_code != expected_status:
            print(f"   Expected: {expected_status}, Got: {response.status_code}")
            print(f"   Response: {response.text[:200]}...")
        
        return response.json() if response.content else {}
        
    except requests.exceptions.ConnectionError:
        print(f"❌ Connection failed to {url}")
        print("   Make sure the server is running: python run.py")
        return None
    except Exception as e:
        print(f"❌ Error testing {method} {endpoint}: {str(e)}")
        return None

def run_comprehensive_tests():
    """Run comprehensive system tests."""
    print("🧪 Starting Alerting Platform System Tests")
    print("=" * 50)
    
    # Test 1: System Health
    print("\n📊 Testing System Health...")
    health = test_api_endpoint('GET', '/api/analytics/system/health')
    if health and health.get('system_health', {}).get('overall_status') == 'healthy':
        print("✅ System is healthy")
    else:
        print("⚠️  System health check failed")
    
    # Test 2: Admin APIs
    print("\n👨‍💼 Testing Admin APIs...")
    
    # List users
    users_response = test_api_endpoint('GET', '/api/admin/users')
    if users_response and 'users' in users_response:
        users = users_response['users']
        admin_users = [u for u in users if u['is_admin']]
        regular_users = [u for u in users if not u['is_admin']]
        print(f"   Found {len(users)} users ({len(admin_users)} admins, {len(regular_users)} regular)")
    
    # List teams
    teams_response = test_api_endpoint('GET', '/api/admin/teams')
    if teams_response and 'teams' in teams_response:
        teams = teams_response['teams']
        print(f"   Found {len(teams)} teams")
    
    # List alerts
    alerts_response = test_api_endpoint('GET', '/api/admin/alerts')
    if alerts_response and 'alerts' in alerts_response:
        alerts = alerts_response['alerts']
        active_alerts = [a for a in alerts if a['is_active']]
        print(f"   Found {len(alerts)} alerts ({len(active_alerts)} active)")
    
    # Test 3: Create New Alert
    print("\n➕ Testing Alert Creation...")
    if admin_users:
        admin_id = admin_users[0]['id']
        new_alert_data = {
            "title": "Test Alert - System Check",
            "message": "This is a test alert created by the system test script.",
            "severity": "info",
            "visibility_type": "organization",
            "created_by": admin_id,
            "expiry_time": (datetime.utcnow() + timedelta(hours=24)).isoformat() + "Z"
        }
        
        create_response = test_api_endpoint('POST', '/api/admin/alerts', new_alert_data, 201)
        if create_response and create_response.get('success'):
            test_alert_id = create_response['alert']['id']
            print(f"   Created test alert with ID: {test_alert_id}")
            
            # Test updating the alert
            update_data = {
                "severity": "warning",
                "message": "Updated test message"
            }
            test_api_endpoint('PUT', f'/api/admin/alerts/{test_alert_id}', update_data)
            
            # Test archiving the alert
            test_api_endpoint('POST', f'/api/admin/alerts/{test_alert_id}/archive')
            print("   Cleaned up test alert")
    
    # Test 4: User APIs
    print("\n👤 Testing User APIs...")
    if regular_users:
        test_user = regular_users[0]
        user_id = test_user['id']
        
        # Get user alerts
        user_alerts = test_api_endpoint('GET', f'/api/user/alerts?user_id={user_id}')
        if user_alerts and 'alerts' in user_alerts:
            alerts_count = len(user_alerts['alerts'])
            print(f"   User {test_user['name']} has {alerts_count} visible alerts")
            
            # Test user dashboard
            dashboard = test_api_endpoint('GET', f'/api/user/dashboard?user_id={user_id}')
            if dashboard and 'summary' in dashboard:
                summary = dashboard['summary']
                print(f"   Dashboard: {summary['unread_count']} unread, {summary['read_count']} read, {summary['snoozed_count']} snoozed")
            
            # Test alert interactions if there are alerts
            if alerts_count > 0:
                alert_id = user_alerts['alerts'][0]['id']
                
                # Test marking as read
                test_api_endpoint('POST', f'/api/user/alerts/{alert_id}/read', {'user_id': user_id})
                
                # Test snoozing
                test_api_endpoint('POST', f'/api/user/alerts/{alert_id}/snooze', {'user_id': user_id})
                
                # Test marking as unread
                test_api_endpoint('POST', f'/api/user/alerts/{alert_id}/unread', {'user_id': user_id})
                
                print("   Tested alert interactions (read/snooze/unread)")
    
    # Test 5: Analytics APIs
    print("\n📈 Testing Analytics APIs...")
    
    # Overview
    overview = test_api_endpoint('GET', '/api/analytics/overview')
    if overview and 'overview' in overview:
        ov = overview['overview']
        print(f"   System overview: {ov['alerts']['total']} total alerts, {ov['users']['total_users']} users")
    
    # Alert performance
    test_api_endpoint('GET', '/api/analytics/alerts/performance?limit=10')
    
    # Daily trends
    test_api_endpoint('GET', '/api/analytics/trends/daily?days=7')
    
    # User engagement
    test_api_endpoint('GET', '/api/analytics/users/engagement?limit=10')
    
    # Test 6: Notification History
    print("\n📜 Testing Notification History...")
    if regular_users:
        user_id = regular_users[0]['id']
        history = test_api_endpoint('GET', f'/api/user/notifications/history?user_id={user_id}&per_page=5')
        if history and 'deliveries' in history:
            print(f"   Found {len(history['deliveries'])} notification deliveries")
    
    # Test 7: System Statistics
    print("\n📊 Testing System Statistics...")
    stats = test_api_endpoint('GET', '/api/admin/stats/system')
    if stats:
        print("   Retrieved system statistics successfully")
    
    print("\n" + "=" * 50)
    print("🎉 System Tests Completed!")
    print("\nNext steps:")
    print("1. Check the application logs for any errors")
    print("2. Test the reminder system by waiting 2 hours or triggering manually")
    print("3. Create alerts with different visibility types")
    print("4. Test with different user accounts")
    print("\nFor manual testing, use the sample admin account:")
    print("- Email: admin@example.com")
    print("- Create alerts via: POST /api/admin/alerts")

def test_reminder_system():
    """Test the reminder system functionality."""
    print("\n⏰ Testing Reminder System...")
    
    # Get active alerts
    alerts_response = test_api_endpoint('GET', '/api/admin/alerts?status=active')
    if alerts_response and 'alerts' in alerts_response:
        active_alerts = alerts_response['alerts']
        
        if active_alerts:
            # Try to trigger a manual reminder for the first active alert
            alert_id = active_alerts[0]['id']
            reminder_response = test_api_endpoint('POST', f'/api/admin/alerts/{alert_id}/send-reminder')
            
            if reminder_response and reminder_response.get('success'):
                print(f"   ✅ Successfully triggered reminder for alert {alert_id}")
                print(f"   Sent {reminder_response.get('reminders_sent', 0)} reminders")
            else:
                print("   ⚠️  Reminder trigger failed or no users needed reminders")
        else:
            print("   ℹ️  No active alerts found to test reminders")

if __name__ == '__main__':
    print("🚀 Alerting & Notification Platform - System Test")
    print("Make sure the server is running with: python run.py")
    print()
    
    # Wait a moment for user to see the message
    time.sleep(2)
    
    # Run the tests
    run_comprehensive_tests()
    
    # Test reminder system
    test_reminder_system()
    
    print(f"\n✨ All tests completed at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}") 