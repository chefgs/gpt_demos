export default function Robots() {
    return (
        `User-agent: *
        Allow: /

        Sitemap: https://yourdomain.com/api/sitemap`
    );
}

export async function getServerSideProps({ res }) {
    res.setHeader('Content-Type', 'text/plain');
    res.write(`User-agent: *
Allow: /

Sitemap: https://yourdomain.com/api/sitemap`);
    res.end();

    return { props: {} };
}
