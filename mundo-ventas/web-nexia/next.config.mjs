/** @type {import('next').NextConfig} */
const nextConfig = {
  output: "export",   // static export → deployable to Netlify/GitHub Pages gratis
  trailingSlash: true,
};

export default nextConfig;
