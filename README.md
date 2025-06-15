# Flask Waste Classification App

## Struktur Project
```
|
├── model\
|   └──mobilenet_best.h5 
├── resources\
|   └── images\
|   └── images_results\
├── venv\
├── views\
│   └── index.html 
├── .gitignore    
├── cv-deployment.py  
└── README.md
```

## Installation & Setup

### 1. Install venv
Install dependencies:
```bash
python -m venv venv
```
### 2. Install Dependencies
masuk ke virtual environtment:

windows:
```bash
venv\Scripts\activate
```

linux/macOs:
```bash
venv/bin/activate
```

Install dependencies:
```bash
pip install -r requirements.txt
```

### 3. Setup Model

- Pastikan file model `mobilenet_best.h5` ada di folder root
- Atau ubah path model di `cv-development.py` line 38:
```python
loaded_model = tf.keras.models.load_model('model\mobilenet_best.h5')
```

### 4. Run Application

```bash
python cv-deployment.py
```

Aplikasi akan berjalan di `http://localhost:5000`

## Features

### 🖼️ **Interactive Upload Interface**
- Drag & drop support
- File validation
- Progress indicators
- Modern UI design

### 🤖 **AI Classification**
- Real-time waste classification
- Confidence scoring
- Visual bounding box overlay
- 9 waste categories support

### 📊 **Result Visualization**
- Color-coded bounding boxes
- Confidence percentages
- Complete prediction breakdown
- Downloadable result images

### 📱 **Responsive Design**
- Mobile-friendly interface
- Touch-optimized controls
- Adaptive layouts

## API Endpoints

### `GET /`
Homepage dengan upload interface

### `POST /predict`
Upload dan classify image

**Request:**
- Method: POST
- Content-Type: multipart/form-data
- Body: image file

**Response:**
```json
{
    "predicted_class": "Glass",
    "confidence": 95.67,
    "all_predictions": {
        "Glass": 95.67,
        "Plastic": 2.34,
        "Metal": 1.23,
        ...
    },
    "result_image": "results/result_image.jpg",
    "color": "#00CED1"
}
```

## Waste Categories

| Category            | Color                                                                 | Description                    |
|---------------------|------------------------------------------------------------------------|--------------------------------|
| Cardboard           | <span style="display:inline-block;width:20px;height:20px;background:#8B4513;border-radius:4px;"></span> `#8B4513` | Cardboard boxes, packaging     |
| Food Organics       | <span style="display:inline-block;width:20px;height:20px;background:#228B22;border-radius:4px;"></span> `#228B22` | Food waste, organic materials  |
| Glass               | <span style="display:inline-block;width:20px;height:20px;background:#00CED1;border-radius:4px;"></span> `#00CED1` | Glass bottles, containers      |
| Metal               | <span style="display:inline-block;width:20px;height:20px;background:#C0C0C0;border-radius:4px;"></span> `#C0C0C0` | Metal cans, containers         |
| Miscellaneous Trash | <span style="display:inline-block;width:20px;height:20px;background:#696969;border-radius:4px;"></span> `#696969` | Mixed waste materials          |
| Paper               | <span style="display:inline-block;width:20px;height:20px;background:#F5F5DC;border-radius:4px;"></span> `#F5F5DC` | Paper documents, newspapers    |
| Plastic             | <span style="display:inline-block;width:20px;height:20px;background:#FF6347;border-radius:4px;"></span> `#FF6347` | Plastic bottles, containers    |
| Textile Trash       | <span style="display:inline-block;width:20px;height:20px;background:#9370DB;border-radius:4px;"></span> `#9370DB` | Clothing, fabric materials     |
| Vegetation          | <span style="display:inline-block;width:20px;height:20px;background:#32CD32;border-radius:4px;"></span> `#32CD32` | Plant matter, garden waste     |



## Customization

### Menambah Category Baru
1. Update `class_labels` list di `cv-deployment.py`
2. Tambahkan warna di `class_colors` dictionary
3. Update kategori di template `index.html`
4. Retrain model dengan kategori baru

### Mengubah Model
Ganti model di `cv-deployment.py`:
```python
loaded_model = tf.keras.models.load_model('your_new_model.h5')
```

### Styling Customization
Edit CSS di `templates/index.html` untuk mengubah tampilan.

## Deployment Options

### Local Development
```bash
python cv-deployment.py
```

### Production with Gunicorn
```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

### Docker Deployment
```dockerfile
FROM python:3.9-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
EXPOSE 5000

CMD ["python", "cv-deployment.py"]
```

## Performance Tips

1. **Model Optimization**: Use TensorFlow Lite untuk model yang lebih kecil
2. **Image Caching**: Implement Redis untuk cache hasil prediksi
3. **Background Processing**: Gunakan Celery untuk processing async
4. **CDN**: Serve static files via CDN untuk production

## Security Considerations

- File size limits (16MB default)
- File type validation
- Secure filename handling
- Input sanitization
- Rate limiting (recommended untuk production)

## Troubleshooting

### Model Loading Error
```bash
# Check TensorFlow version compatibility
pip install tensorflow==2.13.0
```

### Memory Issues
```bash
# Reduce batch size atau image size
# Add memory limits di Docker
```

### Port Already in Use
```bash
# Change port in cv-deployment.py
app.run(debug=True, host='0.0.0.0', port=5001)
```

## Contributing

1. Fork repository
2. Create feature branch
3. Commit changes
4. Push to branch
5. Create Pull Request