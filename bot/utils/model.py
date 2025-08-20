
import cv2
import numpy as np
import matplotlib.pyplot as plt
from sklearn.metrics.pairwise import euclidean_distances

class ScoliosisAnalyzer:
    def init(self):
        self.landmarks = []
        self.asymmetry_score = 0
        self.curvature_angle = 0
        
    def preprocess_image(self, image_path):
        """Предварительная обработка изображения"""
        image = cv2.imread(image_path)
        if image is None:
            raise ValueError("Не удалось загрузить изображение")
        
        # Конвертация в оттенки серого
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        
        # Улучшение контраста
        clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
        enhanced = clahe.apply(gray)
        
        # Размытие для уменьшения шума
        blurred = cv2.GaussianBlur(enhanced, (5, 5), 0)
        
        return image, blurred
    
    def detect_spine_landmarks(self, image, processed_image):
        """Обнаружение ключевых точек позвоночника"""
        # Простой детектор краев
        edges = cv2.Canny(processed_image, 50, 150)
        
        # Поиск контуров
        contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        # Фильтрация контуров по размеру
        large_contours = [cnt for cnt in contours if cv2.contourArea(cnt) > 1000]
        
        landmarks = []
        for contour in large_contours:
            # Аппроксимация контура
            epsilon = 0.02 * cv2.arcLength(contour, True)
            approx = cv2.approxPolyDP(contour, epsilon, True)
            
            for point in approx:
                x, y = point[0]
                landmarks.append((x, y))
        
        return landmarks
    
    def calculate_asymmetry(self, landmarks, image_width):
        """Расчет асимметрии позвоночника"""
        if not landmarks:
            return 0
        
        # Разделение точек на левую и правую половины
        mid_x = image_width // 2
        left_points = [p for p in landmarks if p[0] < mid_x]
        right_points = [p for p in landmarks if p[0] > mid_x]
        
        if not left_points or not right_points:
            return 0
        
        # Расчет средней линии
        left_center = np.mean(left_points, axis=0)
        right_center = np.mean(right_points, axis=0)
        
        # Оценка асимметрии
        horizontal_diff = abs(left_center[0] - (image_width - right_center[0]))
        vertical_diff = abs(left_center[1] - right_center[1])
        
        asymmetry_score = (horizontal_diff + vertical_diff) / image_width * 100
        
        return asymmetry_score
    
    def estimate_curvature(self, landmarks):
        """Оценка кривизны позвоночника"""
        if len(landmarks) < 3:
            return 0
        
        # Сортировка точек по вертикали
        sorted_points = sorted(landmarks, key=lambda x: x[1])
        
        # Выбор верхней, средней и нижней точек
        top = sorted_points[0]
        middle = sorted_points[len(sorted_points)//2]
        bottom = sorted_points[-1]
        
        # Расчет угла кривизны
        vec1 = np.array([middle[0] - top[0], middle[1] - top[1]])
        vec2 = np.array([bottom[0] - middle[0], bottom[1] - middle[1]])
        
        dot_product = np.dot(vec1, vec2)
        mag1 = np.linalg.norm(vec1)  # Исправлено здесь
        mag2 = np.linalg.norm(vec2)  # Исправлено здесь
        
        if mag1 == 0 or mag2 == 0:
            return 0
        
        cos_angle = dot_product / (mag1 * mag2)
        angle_rad = np.arccos(np.clip(cos_angle, -1.0, 1.0))
        angle_deg = np.degrees(angle_rad)
        
        return angle_deg
    
    def analyze_scoliosis(self, image_path):
        """Основной метод анализа"""
        try:
            # Загрузка и предобработка изображения
            original, processed = self.preprocess_image(image_path)
            height, width = original.shape[:2]
            
            # Обнаружение ключевых точек
            landmarks = self.detect_spine_landmarks(original, processed)
            self.landmarks = landmarks

# Расчет показателей
            self.asymmetry_score = self.calculate_asymmetry(landmarks, width)
            self.curvature_angle = self.estimate_curvature(landmarks)
            
            # Определение вероятности сколиоза
            probability = self.calculate_probability()
            
            return {
                'asymmetry_score': self.asymmetry_score,
                'curvature_angle': self.curvature_angle,
                'probability': probability,
                'landmarks_count': len(landmarks)
            }
            
        except Exception as e:
            return {'error': str(e)}
    
    def calculate_probability(self):
        """Расчет вероятности сколиоза"""
        prob = min(100, max(0, 
            (self.asymmetry_score * 2) + 
            (max(0, self.curvature_angle - 10) * 1.5)
        ))
        return prob
    
    def visualize_results(self, image_path, output_path=None):
        """Визуализация результатов анализа"""
        original = cv2.imread(image_path)
        if original is None:
            return
        
        for point in self.landmarks:
            cv2.circle(original, tuple(point), 5, (0, 255, 0), -1)
        
        height, width = original.shape[:2]
        cv2.line(original, (width//2, 0), (width//2, height), (255, 0, 0), 2)
        
        text = f"Asymmetry: {self.asymmetry_score:.1f}% | Curvature: {self.curvature_angle:.1f}°"
        cv2.putText(original, text, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 
                   0.7, (0, 0, 255), 2)
        
        if output_path:
            cv2.imwrite(output_path, original)
        
        return original
