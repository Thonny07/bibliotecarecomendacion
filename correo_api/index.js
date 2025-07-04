const express = require("express");
const nodemailer = require("nodemailer");
const cors = require("cors");
const bodyParser = require("body-parser");

const app = express();
app.use(cors());
app.use(bodyParser.json());

app.post("/enviar-correo", async (req, res) => {
  const { destinatario, codigo } = req.body;

  // Configura tu cuenta Gmail o de otro servicio
  const transporter = nodemailer.createTransport({
    service: "gmail",
    auth: {
      user: "anthonymoraavalos7@gmail.com ", // tu correo
      pass: "otsr swfu vjew fzbb", // tu contraseña de aplicación
    },
  });

  const mailOptions = {
    from: "Biblioteca Alexandrina <anthonymoraavalos7@gmail.com >",
    to: destinatario,
    subject: "🔑 Código de recuperación - Biblioteca Alexandrina",
    text: `Tu código de recuperación es: ${codigo}`,
  };

  try {
    await transporter.sendMail(mailOptions);
    res.status(200).json({ mensaje: "Correo enviado correctamente" });
  } catch (error) {
    console.error("Error al enviar correo:", error);
    res.status(500).json({ mensaje: "Error al enviar el correo", error });
  }
});

app.listen(3001, () => {
  console.log("Servidor de correo escuchando en http://localhost:3001");
});
