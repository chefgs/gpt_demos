import Link from 'next/link';

const BlogLink = ({ filename }) => {
    return (
        <li>
            <Link href={`/blogs/${filename}`} legacyBehavior>
                <a>{filename.replace(/-/g, ' ')}</a>
            </Link>
        </li>
    );
};

export default BlogLink;
