import Head from 'next/head';

const SEO = ({ title, description, keywords, image, url }) => {
    const jsonLd = {
        "@context": "https://schema.org",
        "@type": "Article",
        "headline": title,
        "image": image,
        "author": {
            "@type": "Organization",
            "name": "The Great Technology Company"
        },
        "publisher": {
            "@type": "Organization",
            "name": "The Great Technology Company",
            "logo": {
                "@type": "ImageObject",
                "url": "/images/logo.png"
            }
        },
        "datePublished": "2024-05-19",
        "description": description,
        "mainEntityOfPage": url
    };

    return (
        <Head>
            <title>{title}</title>
            <meta name="description" content={description} />
            <meta name="keywords" content={keywords} />
            <meta property="og:title" content={title} />
            <meta property="og:description" content={description} />
            <meta property="og:image" content={image} />
            <meta property="og:url" content={url} />
            <meta name="twitter:title" content={title} />
            <meta name="twitter:description" content={description} />
            <meta name="twitter:image" content={image} />
            <meta name="twitter:card" content="summary_large_image" />
            <link rel="canonical" href={url} />
            <script type="application/ld+json" dangerouslySetInnerHTML={{ __html: JSON.stringify(jsonLd) }} />
        </Head>
    );
};

export default SEO;
