from fasthtml.common import *  # type: ignore

js_scripts = Script(
    """
function scrollToBottom() {
    var chatlist = document.getElementById('chatlist');
    chatlist.scrollTop = chatlist.scrollHeight;
}

function toggleSidebar() {
    const sidebar = document.getElementById('sidebar');
    const navbarOpenBtn = document.getElementById('navbar-open-btn');
    const sidebarCloseBtn = document.getElementById('sidebar-close-btn');
    
    if (sidebar.classList.contains('w-0')) {
        // Open sidebar
        sidebar.classList.remove('w-0');
        sidebar.classList.add('w-64');
        navbarOpenBtn.classList.add('hidden');
    } else {
        // Close sidebar
        sidebar.classList.remove('w-64');
        sidebar.classList.add('w-0');
        navbarOpenBtn.classList.remove('hidden');
    }
}

// Initialize sidebar state on page load
window.addEventListener('load', function() {
    const sidebar = document.getElementById('sidebar');
    const navbarOpenBtn = document.getElementById('navbar-open-btn');
    const sidebarCloseBtn = document.getElementById('sidebar-close-btn');

    if (sidebar.classList.contains('w-64')) {
        navbarOpenBtn.classList.add('hidden');
        sidebarCloseBtn.classList.remove('hidden');
    }
});

"""
)
