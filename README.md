# PoseBrew

- [Switch to English](README_en.md)  
- Русский (выбран)

## Курсовая работа, ВМК МГУ (2025 год) <br>
В процессе работы был разработан End-to-End инструмент, позволяющий провести оценку относительной трехмерной позы человека на основе произвольного (in-the-wild) .mp4 видео. Теоретическое описание может быть найдено в [тексте курсовой](). 

#### Технические требования
Инструмент разработан под ОС Windows. <br>
Для использования требуется наличие: [python](https://www.python.org/downloads/), [git](https://git-scm.com/downloads), [conda](https://docs.conda.io/projects/conda/en/latest/user-guide/install/index.html)

Работа была протестирована на системе:
- ОС: Windows 11 x64
- CPU: AMD Ryzen 5 7535HS
- GPU: не использовалась (работа производится в CPU-only режиме для совместимости с системами без поддержки CUDA)
- RAM: 16 GB

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
##### Получить анимации и 3D точки по одному видео: <br>
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

##### Предсказания в мультикамерной конфигурации: <br>
```
infer file1 file2 [--npy] [--synced]
```
Если file1 и file2 есть .npy файлы, то предсказание не требуется - выполняется только слияние трехмерных точек. В таком случае требуется указать флаг --npy <br>
Если file1 и file2 есть .mp4 файлы, то сначала выполняется предсказание на обоих файлах, затем -- слияние

    
В процессе генерируются следующие файлы и папки:
- mmpose_output\output_filename (2D точки)
- boxmot_output\filename.mp4 (анимация трекинга)
- motionbert_output\filename_0 (3D точки и анимации до ансамблирования, без сдвига)
- motionbert_output\filename_1 (3D точки и анимации до ансамблирования, сдвиг на 1 шаг)
- motionbert_output\filename_2 (3D точки и анимации до ансамблирования, сдвиг на 2 шага)

Итоговый результат:
- animations\filename_monocular_animation.mp4 (анимация 3D точек на выходе)
- predictions\filename.npy (3D точки на выходе)


