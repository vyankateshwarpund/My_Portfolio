// GitHub API Integration
document.addEventListener('DOMContentLoaded', () => {
    fetchGitHubStats();
});

function fetchGitHubStats() {
    const githubUser = 'vyankateshwarpund';
    const repoCountEl = document.getElementById('gh-repo-count');
    const followersCountEl = document.getElementById('gh-followers-count');

    fetch(`https://api.github.com/users/${githubUser}`)
        .then(res => {
            if (!res.ok) throw new Error('GitHub API Limit or Network Issue');
            return res.json();
        })
        .then(data => {
            if (repoCountEl) repoCountEl.textContent = data.public_repos || '15+';
            if (followersCountEl) followersCountEl.textContent = data.followers || '25+';
        })
        .catch(err => {
            console.log('GitHub API fallback active');
        });
}
