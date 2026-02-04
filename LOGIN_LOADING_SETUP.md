# Login Loading Screen Setup Instructions

## Image Setup Required

The login loading screen is now implemented and ready to work, but you need to save the actual "STAY FOCUSED" image file.

### Steps:
1. Save the "STAY FOCUSED" image you provided as: `stay_focused.webp`
2. Place it in the directory: `static/images/`
3. The file should replace the current placeholder

### What Happens:
- When users click "Log in", the loading screen immediately appears
- Shows the full-screen "STAY FOCUSED" image with fade and zoom animations
- Displays a white progress bar at the bottom that fills over 2.5 seconds
- Uses smooth transitions and minimal design as requested

### Features:
- ✅ Full screen black background
- ✅ Centered "STAY FOCUSED" image with animations
- ✅ White progress bar at bottom
- ✅ Fade and zoom animations
- ✅ Minimal design with no extra elements
- ✅ Responsive for mobile devices
- ✅ Automatic fallback to focus_splash.webp if stay_focused.webp not found

### Testing:
Visit http://127.0.0.1:8000/ and try logging in to see the loading screen in action!

### Image Specifications:
- Format: JPG
- Background: Black
- Text: White "STAY FOCUSED"
- Recommended size: Up to 1920x1080 for best quality