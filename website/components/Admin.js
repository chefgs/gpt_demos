import { useState } from 'react';
import ReactMarkdown from 'react-markdown';

const Admin = () => {
    const [title, setTitle] = useState('');
    const [content, setContent] = useState('');

    const handleSubmit = async (e) => {
        e.preventDefault();
        const res = await fetch('/api/blogs', {
            method: 'POST',
            body: JSON.stringify({ title, content }),
            headers: { 'Content-Type': 'application/json' },
        });
        if (res.ok) {
            setTitle('');
            setContent('');
            alert('Blog post created successfully');
        } else {
            alert('Error creating blog post');
        }
    };

    return (
        <div>
            <form onSubmit={handleSubmit}>
                <h2>Admin - Add Blog Post</h2>
                <input
                    type="text"
                    placeholder="Title (e.g., new-blog)"
                    value={title}
                    onChange={(e) => setTitle(e.target.value)}
                    required
                />
                <textarea
                    placeholder="Content in Markdown"
                    value={content}
                    onChange={(e) => setContent(e.target.value)}
                    required
                />
                <button type="submit">Add Blog Post</button>
            </form>
            <h2>Preview</h2>
            <ReactMarkdown children={content} />
        </div>
    );
};

export default Admin;