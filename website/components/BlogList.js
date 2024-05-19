import { useEffect, useState } from 'react';
import BlogLink from './BlogLink';

const BlogList = () => {
    const [blogs, setBlogs] = useState([]);

    useEffect(() => {
        const fetchBlogs = async () => {
            const res = await fetch('/api/blogs');
            const data = await res.json();
            setBlogs(data);
        };
        fetchBlogs();
    }, []);

    return (
        <div>
            <h2>Blogs</h2>
            <ul>
                {blogs.map((blog, index) => (
                    <BlogLink key={index} filename={blog.filename} />
                ))}
            </ul>
        </div>
    );
};

export default BlogList;
