import fs from 'fs';
import path from 'path';

const postsDirectory = path.join(process.cwd(), 'posts');

export default function handler(req, res) {
    if (req.method === 'GET') {
        const filenames = fs.readdirSync(postsDirectory);
        const posts = filenames.map(filename => {
            const filePath = path.join(postsDirectory, filename);
            const fileContents = fs.readFileSync(filePath, 'utf8');
            return {
                filename: filename.replace(/\\.md$/, ''),
                content: fileContents
            };
        });
        res.status(200).json(posts);
    } else if (req.method === 'POST') {
        const { filename, content } = req.body;
        const filePath = path.join(postsDirectory, `${filename}.md`);
        fs.writeFileSync(filePath, content, 'utf8');
        res.status(201).json({ message: 'Blog post created' });
    } else {
        res.status(405).json({ message: 'Method not allowed' });
    }
}
