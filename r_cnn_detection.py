import cv2
import torchvision.models as models
from torchvision import transforms
import torch

# Порог в кадрах, после которого чашка будет считаться потерянной из области видимости
ABSENT_THRSH = 5


# Функция, которая на вход принимает расположение видео
# и расположение папки в которое обработанное видео будет записано
def detect_cup(file_path, out_folder):
    cap = cv2.VideoCapture(file_path)

    # Проверка того что видео было успешно открыто
    if (cap.isOpened() == False):
        print("Error opening video stream or file")

    # Установка кодека и разрешения для видео
    fourcc = cv2.VideoWriter_fourcc(*'VP80')
    frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    out = cv2.VideoWriter(out_folder, fourcc, 14.0, (frame_width, frame_height))
    # Если доступна видеокарта, то обрабатываем видео через нее
    device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
    model = models.detection.fasterrcnn_resnet50_fpn(pretrained=True).to(device)
    model.eval()
    # Объявляем счетчики. Кол-во кадров на котором чашка отсутствует, а так же порядковый номер присутствия/осутствия
    # чашки на кадре (нужно для имени сохраненного файла)
    dropped_frames = 0
    absent_num = 0
    presence_num = 0

    # Чтение кадров из видео
    while (cap.isOpened()):

        ret, frame = cap.read()
        if ret == True:

            # Преобразовываем изображение в тензор
            img = transforms.ToTensor()(frame).to(device)[:3]

            # Прогоняем изображение через модель, 47 это метка чашки в СОСО датасете
            predict = model(img.unsqueeze(0))[0]
            cups_loc_ids = (predict['labels'] == 47).nonzero()

            # Проверяем на то есть ли чашка в предсказаниях
            if len(cups_loc_ids) != 0:

                # Если чашек модель предсказала несколько, то берем предсказание с наибольшей "уверенностью"
                if len(cups_loc_ids) > 1:
                    best_score = predict['scores'][cups_loc_ids].max()
                    best_score_id = (predict['scores'] == best_score).nonzero()[0]
                else:
                    best_score_id = cups_loc_ids[0]
                # Отрисовываем bounding box
                bbox = predict['boxes'][best_score_id][0]
                cv2.rectangle(frame, (bbox[0], bbox[1]), (bbox[2], bbox[3]), (255, 0, 0), 2)
                # Если кол-во кадров на котором чашка отсутствует >= threshold это сведельствует о том
                # что чашка появилась в кадре, поэтому сохраняем изображение
                if dropped_frames >= ABSENT_THRSH:
                    presence_num += 1
                    cv2.rectangle(frame, (bbox[0], bbox[1]), (bbox[2], bbox[3]), (255, 0, 0), 2)
                    cv2.imwrite("static/imgs/presence/{}.png".format(presence_num), frame)
                # Обнуляем счетчик потерянных кадров
                dropped_frames = 0

                # Записываем обработанный кадр в видео
                out.write(frame)

            else:
                # Если кол-во кадров в котором чашка отстутствует становится равна threshold
                # это означает что чашка вышла из кадра, поэтому мы сохраняем изображение
                if dropped_frames == ABSENT_THRSH:
                    absent_num += 1
                    cv2.putText(frame, 'CUP IS HIDING', (300, 500), cv2.FONT_HERSHEY_SIMPLEX, 4.0, (0, 0, 255), 3)
                    cv2.imwrite("static/imgs/absent/{}.png".format(absent_num), frame)
                # Обновляем счетчик потерянных кадров и записывем обработанный кадр в видео
                dropped_frames += 1
                out.write(frame)
            if cv2.waitKey(25) & 0xFF == ord('q'):
                break

        else:
            break

    cap.release()