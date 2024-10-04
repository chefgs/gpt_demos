import Layout from '../../components/Layout';
import BlogList from '../../components/BlogList';
import SEO from '../../components/SEO';

export default function Blogs() {
    return (
        <Layout>
            <SEO
                title="Blogs - The Great Technology Company"
                description="Read the latest blogs from The Great Technology Company on cloud engineering and DevOps automation."
                keywords="Blogs, Cloud, DevOps, Automation"
                image="/images/logo.png"
                url="https://yourdomain.com/blogs"
            />
            <BlogList />
        </Layout>
    );
}
