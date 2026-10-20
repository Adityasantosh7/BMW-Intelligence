import './globals.css';

export const metadata = {
  title: 'BMW Intelligence',
  description: 'BMW vehicle intelligence dashboard',
};

export default function RootLayout({ children }) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}
