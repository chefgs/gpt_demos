import { useState } from 'react';

const Admin = () => {
    const [filename, setFilename] = useState('');
    const [content, setContent] = useState('');

    const handleSubmit = async (e) => {
        e.preventDefault();
        const res = await fetch('/api/blogs', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ filename, content }),
        });
        if (res.ok) {
            setFilename('');
            setContent('');
            alert('Blog post created');
        } else {
            alert('Error creating blog post');
        }
    };

    return (
        <form onSubmit={handleSubmit}>
            <h2>Admin - Add Blog Post</h2>
            <input
                type="text"
                placeholder="Filename (e.g., new-blog)"
                value={filename}
                onChange={(e) => setFilename(e.target.value)}
                required
            />
            <textarea
                placeholder="Blog Content"
                value={content}
                onChange={(e) => setContent(e.target.value)}
                required
            ></textarea>
            <button type="submit">Add Blog Post</button>
        </form>
    );
};

export default Admin;
