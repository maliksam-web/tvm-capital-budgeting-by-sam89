/**
 * HARDENED WEBVIEW GESTURE INTERCEPTOR ENGINE
 * Blocks browser context pull-to-refresh routines at the ceiling boundary.
 */
(function() {
    let touchStartOffsetY = 0;
    
    window.addEventListener('touchstart', function(event) {
        if (event.touches.length === 1) {
            touchStartOffsetY = event.touches[0].clientY;
        }
    }, { passive: false });

    window.addEventListener('touchmove', function(event) {
        if (event.touches.length === 1) {
            let touchCurrentOffsetY = event.touches[0].clientY;
            let axisDiffY = touchCurrentOffsetY - touchStartOffsetY;
            
            // If the user's viewport is at the ceiling (0) and dragging downward, kill the action
            if (window.scrollY === 0 && axisDiffY > 0) {
                event.preventDefault();
            }
        }
    }, { passive: false });
})();

