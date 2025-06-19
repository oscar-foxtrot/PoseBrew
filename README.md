# PoseBrew

- [Switch to English](README_en.md)  
- Русский (выбран)

## Курсовая работа, ВМК МГУ (2025 год) <br>
В процессе работы был разработан End-to-End инструмент, позволяющий провести оценку относительной трехмерной позы человека на основе произвольного (in-the-wild) .mp4 видео. Теоретическое описание приведено в [тексте курсовой](https://github.com/oscar-foxtrot/posebrew-pose3d-coursework/blob/main/coursework_oscar.pdf). 

#### Технические требования
Инструмент разработан под ОС Windows. <br>
Для использования требуется наличие: [python](https://www.python.org/downloads/), [git](https://git-scm.com/downloads), [conda](https://docs.conda.io/projects/conda/en/latest/user-guide/install/index.html)

### Инструкция по установке <br>
Откройте Anaconda Prompt (или терминал с активированным conda).  
Далее:
```
git clone https://github.com/oscar-foxtrot/PoseBrew
cd PoseBrew
```
Следующая команда автоматически проведет установку библиотек и настройку рабочего окружения <br>
(ожидаемое время ~20-30 минут, место на диске ~9 GB):
```
setup
```

### Оценка позы <br>
##### Получить анимации и 3D точки по одному видео:
```
infer filename.mp4
```

В процессе генерируются следующие файлы и папки:
- mmpose_output\output_filename (2D точки)
- boxmot_output\filename.mp4 (анимация трекинга)
- motionbert_output\filename_0 (3D точки и анимации до ансамблирования, без сдвига)
- motionbert_output\filename_1 (3D точки и анимации до ансамблирования, сдвиг на 1 шаг)
- motionbert_output\filename_2 (3D точки и анимации до ансамблирования, сдвиг на 2 шага)

Итоговый результат:
- animations\filename_monocular_animation.mp4 (анимация 3D точек на выходе)
- predictions\filename.npy (3D точки на выходе)

##### Предсказания в мультикамерной конфигурации:
```
infer file1 file2 [--npy] [--synced]
```
Если file1 и file2 есть .npy файлы, полученные с помощью **infer file1.mp4** и **infer file2.mp4**, то предсказание не требуется - выполняется только слияние трехмерных точек. В таком случае требуется указать флаг **--npy**. <br>
Если file1 и file2 есть .mp4 файлы, то сначала выполняется предсказание на обоих файлах, затем - слияние. Тогда требуется опустить флаг **--npy**. <br>
Если file1 и file2 есть синхронизированные во времени .mp4 или .npy файлы, то требуется дополнительно указать флаг **--synced**. Тогда автоматическая синхронизация не выполняется.

    
В процессе генерируются следующие файлы и папки:
- predictions\file1_aligned.npy (3D точки позы из файла 1, наложенные на точки позы из файла 2)
- predictions\file2_aligned.npy (3D точки позы из файла 2, наложенные на точки позы из файла 1)
- predictions\file1_file2_fused.npy (3D точки, полученные слиянием поз из файлов 1 и 2)

##### Анимировать точки:
```
animate file1.npy [file2.npy]
```
В процессе генерируются следующие файлы и папки:
- animations\file1_monocular_animation.npy (анимация трехмерной позы, если в командной строке передан путь к одному файлу)
- animations\file1_file2_aligned_animation.npy (анимация сразу двух поз на одном графике, если в командной строке указано 2 файла)

### Пример работы:
В папку PoseBrew поместили директорию neurologist, содержащую видео: file_469.mp4 и file_474.mp4. Эта пара видео записана в мультикамерной конфигурации, синхронизация отсутствует. <br> <br>
Сделать предсказание по первому видео:
```
D:\User\PoseBrew> infer neurologist\file_469.mp4
```
Сделать предсказание по второму видео:
```
D:\User\PoseBrew> infer neurologist\file_474.mp4
```
Получить точки, автоматически синхронизированные во времени, а также наложенные наилучшим образом в пространстве:
```
D:\User\PoseBrew> fuse predictions\file_469.npy predictions\file_474.npy --npy
```
Анимировать полученное наложение:
```
D:\User\PoseBrew> animate predictions\file_469_aligned.npy predictions\file_474_aligned.npy
```
Результат: полученная анимация (file_469_aligned_file_474_aligned_aligned_animation.mp4):
![Result](https://raw.githubusercontent.com/oscar-foxtrot/pose3d-coursework/main/assets/file_469_aligned_file_474_aligned_aligned_animation.gif)

### Датасет:
Датасет (11 видео), использованный в работе, можно найти [здесь](https://drive.google.com/drive/u/4/folders/1r1LvgzcUSsAGHxaXMExGOCglrXlOL6oI).

### Результаты:
Результаты обработки всех 11 видео из датасета (включая все промежуточные этапы) можно найти [здесь](https://drive.google.com/drive/folders/1DfhZYNLys-Ts5_5sNaspMypEJd_I7sgN?usp=drive_link).

### Примечания:
Работа была протестирована на двух системах: <br>
1:
- ОС: Windows 11 x64
- CPU: AMD Ryzen 5 7535HS
- GPU: не использовалась (работа производится в CPU-only режиме для совместимости с системами без поддержки CUDA)
- RAM: 16 GB
- conda 24.9.2

2:
- ОС: Windows 10 x64
- CPU: Intel Core i5-7400
- GPU: не использовалась (работа производится в CPU-only режиме для совместимости с системами без поддержки CUDA)
- RAM: 8 GB
- conda 24.11.3

<br>
Предсказание позы на всех 11 видео из датасета может занять 4-5 часов.
