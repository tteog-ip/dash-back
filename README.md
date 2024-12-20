# Integrated Dashboard Backend Server
2023.05.29 ~ 2023.07.19

▶️ <a href="https://github.com/tteog-ip">Redirect to Main README</a>  
▶️ <a href="https://www.youtube.com/watch?si=KIuKK1Q6NHxV8YJf&v=OIytUFc5xk8&feature=youtu.be">Video</a>

<br>

## 🪅 Architecture
<img src="https://github.com/user-attachments/assets/d1bb4582-6de9-486c-b332-900c8cd374bc" style="width:100%; height:auto;">
<img src="https://github.com/user-attachments/assets/ea4a4a07-0f45-4021-b291-60efb07e499d" style="width:100%; height:auto;">

<br>
<br>

## ⚙️ Tech Stack
- **Framework**
  - `Django 4.2.2`
- **Database**
  - `MySQL`
- **Authentication**
  - `djangorestframework-simplejwt`
- **API Development**
  - `Django REST Framework (DRF)`
- **Middleware**
  - `django-cors-headers`
- **Scheduler**
  - `django-apscheduler`

<br>

## 🎭 TroubleShooting
<details>
<summary><b>🧱 AWS Cost Exploerer API 접근 제한</b></summary>
  
> **Problem** : 주관 기관의 비용 지원 정책으로 인해 AWS Cost Explorer API를 포함한 비용 관련 API에 접근할 수 없었습니다.
> 
> **Solution** : AWS 개별 리소스에 API 요청을 보내 실제 비용을 곱해 계산하는 방식으로 데이터를 제공했습니다. 또한, 스케줄러 기능을 활용해 일정 시간마다 비용 데이터가 자동으로 갱신되도록 구현했습니다.
>

</details>
