const QRCode = require('qrcode');
const path = require('path');

exports.generateQRCode = async (req, res) => {
    const { data } = req.body;
    const outputFilePath = path.join(__dirname, '../public/qrcode.png');

    if (!data) {
        return res.status(400).json({ message: 'Data is required' });
    }

    try {
        await QRCode.toFile(outputFilePath, data);
        res.status(200).json({ url: `/qrcode.png` });
    } catch (err) {
        res.status(500).json({ message: 'Error generating QR code', error: err.message });
    }
};
