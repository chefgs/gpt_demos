import fs from 'fs';
import path from 'path';
import matter from 'gray-matter';
import { remark } from 'remark';
import html from 'remark-html';
import Layout from '../../components/Layout';
import SEO from '../../components/SEO';

export default function BlogPost({ content, frontmatter }) {
    const { title = '', description, date, image } = frontmatter;
    const url = `https://yourdomain.com/blogs/${title.replace(/ /g, '-')}`;

    return (
        <Layout>
            <SEO
                title={title}
                description={description}
                keywords="Blog, Cloud, DevOps, Automation"
                image={image}
                url={url}
            />
            <article>
                <h1>{title}</h1>
                <p>{date}</p>
                <div dangerouslySetInnerHTML={{ __html: content }} />
            </article>
        </Layout>
    );
}

export async function getStaticPaths() {
    const postsDirectory = path.join(process.cwd(), 'posts');
    const filenames = fs.readdirSync(postsDirectory);

    const paths = filenames.map((filename) => ({
        params: {
            slug: filename.replace(/\\.md$/, '')
        }
    }));

    return {
        paths,
        fallback: false
    };
}

export async function getStaticProps({ params }) {
    const postsDirectory = path.join(process.cwd(), 'posts');
    const filePath = path.join(postsDirectory, `${params.slug}`);
    const fileContents = fs.readFileSync(filePath, 'utf8');

    const { content, data } = matter(fileContents);
    const processedContent = await remark().use(html).process(content);
    const contentHtml = processedContent.toString();

    return {
        props: {
            content: contentHtml,
            frontmatter: data
        }
    };
}
