"""
https://codegolf.stackexchange.com/questions/23362/sort-characters-by-darkness

Requirements:

    You must use a monospaced font for darkness detection.

    You must find out how many pixels each character takes up. You must actually draw the character and count pixels, i.e. you can't just hardcode pixel amounts.
        As a more concrete rule: if you switched fonts, your program should still work. Furthermore, your program should be able to switch fonts by simply changing a variable or value or string in the code.

    If you use antialiasing, you must count pixels as percentages of a fully black pixel. For example, an rgb(32, 32, 32) pixel will count as 1/8 of a full pixel. Disregard this rule if your characters are not antialiased.

    After counting pixels, you must sort the characters by the amount of pixels, and output them in order.

    This is code-golf, so the shortest code in bytes will win.


"""

import helpers_web as hw

# # import colorama
# # colorama.init()
# # GREEN   = colorama.Fore.GREEN
# # GRAY    = colorama.Fore.LIGHTBLACK_EX
# # RESET   = colorama.Fore.RESET
# # YELLOW  = colorama.Fore.YELLOW
# # RED     = colorama.Fore.RED
# # CYAN    = colorama.Fore.CYAN
# # MAGENTA = colorama.Fore.MAGENTA

import sys
import freetype as F # pip install freetype-py


def _get_tuples_from_string_sorted_by_darkness(raw_input, mono_font_face_ttf):
    
    ####print("_get_tuples_from_string_sorted_by_darkness:", "raw_input    :", raw_input)
    #print("_get_tuples_from_string_sorted_by_darkness:", "mono_font_face_ttf:", mono_font_face_ttf)
    
    f = F.Face(mono_font_face_ttf)
    f.set_char_size(99)
    
    # return sorted tuples
    return sorted(
        [
            (f.load_char(c) or sum(f.glyph.bitmap.buffer), c) for c in raw_input 
        ]
    )
    
def get_string_by_darkness(raw_input, mono_font_face_ttf, distance=0, make_unique=True, make_singular=True, verbose=False):
    
    #raw_input = remove_control_characters(raw_input)
    
    if False:
        count_spaces = raw_input.count(' ')
        count_n = raw_input.count('\n')
        count_t = raw_input.count('\t')
        count_r = raw_input.count('\r')
        count_cc= hw.string_count_control_characters(raw_input)

        print("get_string_by_darkness", "count_spaces :", count_spaces)
        print("get_string_by_darkness", "count_n      :", count_n)
        print("get_string_by_darkness", "count_t      :", count_t)
        print("get_string_by_darkness", "count_r      :", count_r)
        print("get_string_by_darkness", "count_cc     :", count_cc)
    
    print("get_string_by_darkness", "distance     :", distance)
    #print("get_string_by_darkness", "make_unique  :", make_unique)
    #print("get_string_by_darkness", "make_singular:", make_singular)
    
    res_tuples = _get_tuples_from_string_sorted_by_darkness(raw_input, mono_font_face_ttf)
    #print("res_tuples:", "len:", len(res_tuples))
    
    first_string = ''
    for sum, c in res_tuples:
        first_string += c
    
    # could only keep min step
    if distance >= 1:
        new_tuples = []
        next_limit=0
        for val, c in res_tuples:
            if val >= next_limit:
                #print("\t\t", "keep", (val, c))
                new_tuples.append((val, c))
                next_limit = val + distance
            else:
                #print("\t\t", "skip", (val, c))
                pass
        res_tuples = new_tuples
        #print("distance:", "len:", len(res_tuples), "distance", distance)   
        
    else:
        
        # delete doubles
        if make_unique:
            res_tuples = sorted(list(set(res_tuples)))
            #print("make_unique:", len(res_tuples))
            
        # https://stackoverflow.com/questions/59317757/unique-list-of-tuples-by-first-value-of-tuples
        # keep only last brightness value if multiple brights
        if make_singular:
            res_tuples = list(dict(res_tuples).items())
            #print("make_singular:", len(res_tuples))
                 
    if verbose:
        print("final:", "len:", len(res_tuples), *res_tuples, sep="\n\t")
        pass
        
    res_string = ''
    for sum, c in res_tuples:
        res_string += c
        
    print("get_string_by_darkness", "\n", 
          "len:", len(first_string), # hw.dq3_raw(hw.GRAY + first_string + hw.RESET), 
          "-->", "\n", 
          "len:", len(res_string), hw.dq3_raw(hw.GREEN + res_string + hw.RESET))  
      
    return res_string

def half_string(raw_input):
    res_string = ''
    for i, c in enumerate(raw_input):
        if not (i%2):
            res_string += c
            
    print("half_string", "\n", 
          "len:", len(raw_input), # hw.dq3_raw(hw.GRAY + raw_input + hw.RESET), 
          "-->", "\n", 
          "len:", len(res_string), hw.dq3_raw(hw.GREEN + res_string + hw.RESET))  
    
    return res_string
    
    
if __name__ == "__main__":
    
    import helpers_web as hw
    
    # raw_input = "@+.0"
    # raw_input = "karlsruhe.digital"
    # raw_input = """ !"§$%&/()=?{[]}\|<>,.;:-_^°+*#'@€µ"""    
    # raw_input = get_string_by_darkness(raw_input, "fonts/UbuntuMono-B.ttf")   
    # raw_input = half_string(raw_input)
    # raw_input = half_string(raw_input)

    #get_string_by_darkness("karlsruhe.digital ", "fonts/UbuntuMono-B.ttf")   

    # http://www.kanjidamage.com/kanji
    # https://en.wikipedia.org/wiki/List_of_kanji_by_stroke_count
    # https://www.quora.com/How-are-spaces-used-when-writing-in-Japanese
    # https://www.accreditedlanguage.com/languages/hiragana-katakana-kanji-3-alphabets-1-language/
    
    # https://stackoverflow.com/questions/1938639/monospace-unicode-font
    # https://stackoverflow.com/questions/1938639/monospace-unicode-font
    """

        DejaVu Sans Mono: 3289
        Everson Mono: 9671
        Fixedsys Excelsior: 5993
        FreeMono: 4177
        GNU Unifont: 57089
        Lucida Sans Unicode: 1779
        
        
        Fixedsys Excelsior
        Everson Mono
        DejaVu Sans Mono
        Roboto Mono

        https://unicode-table.com/en/
    """

    for text in [
        # "@+.0",
        # "karlsruhe.digital",
        # """ !"§$%&/()=?{[]}\|<>,.;:-_^°+*#'@€µ""",
        #"丁七九了二人入八刀力十又乃万丈三上下丸久亡凡刃千口土士夕大女子寸小山川工己干弓才之巾乞于也々勺不与中丹予互五井仁今介仏元公六内円冗凶分切刈化匹区升午厄及友双反収天太夫孔少尺屯幻弔引心戸手支文斗斤方日月木欠止比毛氏水火父片牛犬王巴允爪牙匂勾乏勿出世付仕代仙他以令兄只史号叶𠮟加占可句司召台古右石四囚凸凹冬処皮奴功巧包去圧庁広刊北半外央失矢尻尼左布平幼弁必打払斥丘未末本札正母民氷永汁氾犯生主玉巨用冊田由甲申白旧旦甘皿目且矛示礼写立市穴它玄辺込弘瓦丼丙叫両争交仮仰仲件任企伏伐休会伝充兆先光全共再刑列劣匠印危各合吉同名后吏吐向回因団在地壮多好如妃妄存宅宇守安寺尽州巡帆年式弐当忙成旨早旬曲有朱朴机朽次死毎気汗汚江池灯灰百竹米糸缶羊羽老考耳肉肌自至舌舟色芋芝虫血行衣西迅字伊旭庄亘圭汐伎臼汎乱亜伯伴伸伺似但位低住佐体何余作克児兵冷初判別利助努励労医即却卵君吟否含吸吹呈呉告困囲図坂均坊坑声壱売妊妙妥妨孝完対寿尾尿局岐希床序廷弟形役忌忍志忘応快我戒戻扱扶批技抄把抑投抗折抜択改攻更杉材村束条来求決汽沈沖没沢災状狂男町社秀私究系肖肝臣良花芳芸見角言谷豆貝赤走足身車辛酉迎近返邦里防麦串李那沙呂杏冶汰肘阪弄沃妖吾园並乳事享京佳併使例侍供依価侮免具典到制刷券刺刻効劾卒卓協参叔取受周味呼命和固国坪垂夜奇奉奔妹妻姉始姓委季学宗官宙定宜宝実尚居屈届岬岳岩岸幸底店府延弦彼往征径忠念怖性怪房所承披抱抵抹押抽担拍拐拒拓拘招拝拠拡放斉昆昇明易昔服杯東松板析林枚果枝枠枢欧武歩殴毒河沸油治沼沿況泊泌法泡波泣泥注泳炉炊炎牧物画的盲直知祈祉空突者肢肥肩肪肯育舎芽苗若苦英茂茎表迫迭述邪邸金長門阻附雨青非奈阿昌虎弥茅拙朋苑於尭旺采侃宛岡玩股呪刹狙妬阜枕拉版乗亭侯侵便係促俊俗保信冒冠則削前勅勇卑南卸厘厚叙咲単哀品型垣城変奏契姻姿威孤客宣室封専屋峠峡巻帝帥幽度建弧待律後怒思怠急恒恨悔括拷拾持指挑挟政故施星映春昨昭是昼枯架柄某染柔柱柳査栄段泉洋洗洞洒津洪活派浄浅海炭点為牲狩独狭珍甚界畑疫発皆皇盆相盾省看県砂研砕祖祝秋科秒窃糾紀約紅美耐肺胃胆背胎胞臭茶草荒荘衷要訂計貞負赴軌軍迷追退送逃逆郊郎重限面革音風飛食首香彦胡虹眉怨咽畏拶柵拭栃訃昧勃侶柿姦修俳俵俸倉個倍倒候借倣値倫倹俺党兼准凍剖剛剣剤勉匿原員哲唆唇唐埋姫娘娠娯夏孫宮宰害宴宵家容射将展峰島差師席帯帰座庫庭弱徐徒従恋恐恥恩恭息恵悟悦悩扇挙振挿捕捜敏料旅既時書朕朗栓校株核根格栽桃案桑桜桟梅殉殊残殺泰流浜浦浪浮浴浸消涙烈特珠班瓶畔留畜畝疲疾病症益真眠砲破神祥秘租秩称竜笑粉粋紋納純紙級紛素紡索翁耕耗胴胸能脂脅脈致航般荷華虐蚊蚕衰被討訓託記財貢起軒辱透逐逓途通逝速造連郡酌配酒針降陛院陣除陥隻飢馬骨高鬼浩栗桂桐拳唄冥挨挫桁恣脊凄芯捉捗酎剝脇哺釜乾偏停健側偵偶偽副剰動勘務唯唱商問啓喝圏域執培基堀堂婆婚婦宿寂寄密尉崇崎崩巣帳常庶康庸張強彩彫得悠患悪悼情惜惨捨据掃授排掘掛採探接控推措掲描救敗教斎斜断旋族曹望械欲殻涯液涼淑淡深混添清渇済渉渋渓猛猟猫率現球理産略異盗盛眺眼票祭移窒窓章笛符第粒粗粘粛粧累細紳紹紺終組経翌習脚脱脳舶船菊菌菓菜著虚蛇蛍術街袋規視訟訪設許訳豚貧貨販責赦軟転逮週進逸部郭郵郷都酔釈野釣閉陪陰陳陵陶陸険隆雪頂魚鳥麻黄黒鹿梨亀淳猪笹渚爽陳淫葛崖苛惧痕頃梗舷斬埼戚羞袖曽堆唾貪捻偉傍傘備割創勝募博善喚喜喪喫営堅堕堤堪報場塀塁塔塚奥婿媒富寒尊尋就属帽幅幾廃廊弾御復循悲惑惰愉慌扉掌提揚換握揮援揺搭敢散敬晩普景晴晶暁暑替最朝期棋棒棚棟森棺植検業極欺款歯殖減渡渦温測港湖湯湾湿満滋無焦然焼煮猶琴番畳疎痘痛痢登着短硝硫硬程税童筆等筋筒答策紫結絞絡給統絵絶腐腕落葉葬蛮衆裁裂装裕補覚訴診証詐詔評詞詠象貫貯貴買貸費貿賀超越距軸軽遂遅遇遊運遍過道達酢量鈍開閑間陽隅隊階随雄集雇雰雲項順飯飲智須萩敦媛嵐椎翔喬巽湧茨椅喉腎痩貼斑喩勤傑催債傷傾働僧勢勧嗣嘆園塊塑塗塩墓夢奨嫁嫌寛寝幕幹廉微想愁意愚愛感慈慎慨戦損搬携搾摂数新暇暖暗棄楼楽歳殿源準溝溶滅滑滝滞漠漢煙照煩献猿環痴盟睡督碁禁福稚節絹継続罪置署群義聖腰腸腹艇蒸蓄虜虞裏裸褐解触試詩詰話該詳誇誉誠豊賃賄資賊跡路跳践較載辞農違遠遣酪酬鈴鉄鉛鉢鉱隔雅零雷電靴預頑頒飼飽飾鼓睦彙詣窟僅嗅傲隙腫嫉塞詮煎羨頓塡溺蜂慄楷賂毀像僕僚嘱塾境増墨奪嫡察寨寡寧層彰徳徴態慕慢憎摘旗暦暮概構様模歌歴滴漁漂漆漏演漫漬漸獄疑碑磁禅禍種稲穀端箇算管精維綱網綿総緑緒練罰聞膜製複誌認誓誘語誤説読豪踊適遭遮酵酷酸銀銃銅銘銭関閣閥際障隠雌雑需静領駄駅駆髪魂鳴鼻熊聡槙漱瑠璃萎裾遜遡箋綻蜜貌辣瘍儀億劇勲器噴墜墳審寮導履幣弊影徹慣慮慰慶憂憤戯摩撃撤撮撲敵敷暫暴槽標権横歓潔潜潟潤潮澄熟熱監盤確稼稿穂窮窯箱範緊線締編緩縁縄罷膚舗舞蔵衝褒誕課調談請論諸諾謁賓賛賜賞賠賦質趣踏輝輩輪遵遷選遺鋭鋳閲震霊養餓駐魅黙駒憧嬉潰稽憬畿餌摯踪嘲緻誰膝箸罵蝟儒凝墾壁壇壊壌奮嬢憩憲憶憾懐擁操整曇橋機激濁濃燃獣獲磨積穏築樹篤糖緯縛縦縫繁膨興薄薦薪薫薬融衛衡親諭諮謀謡賢輸避還鋼錠錬錯録隣隷頭頼館龍錦骸蓋諧醒膳賭諦麺頰錮償優厳嚇懇懲擦擬濯燥爵犠療矯礁縮績繊翼聴覧謄謙講謝謹購轄醜鍛霜頻鮮磯瞳瞭曖韓臆鍵鍋謎闇蔑璧餅曜濫癒癖瞬礎穫簡糧織繕繭翻職臨藩襟覆覇観贈鎖鎮闘離難題額顔顕類騎騒験蔽藤鎌藍鯉顎戴瀬爆璽簿繰羅臓藻識譜警鏡霧韻願髄鯨鶏麗艶蹴麓懸欄競籍議譲醸鐘響騰艦護躍露顧魔鶴櫻襲驚籠攣龕鑑靨鷹魘鬱驫鸞麤䯂",
        #"ぁあぃいぅうぇえぉおかがきぎくぐけげこごさざしじすずせぜそぞただちぢっつづてでとどなにぬねのはばぱひびぴふぶぷへべぺほぼぽまみむめもゃやゅゆょよらりるれろゎわゐゑをんゔゕゖ゙゚゛゜ゝゞゟ",
        #"アイウエオカキクケコサシスセソタチツテトナニヌネノハヒフヘホマミムメモヤユヨラリルレロワヰヱヲン",
        # # # "アイウエオカキクケコガギグゲゴサシスセソザジズゼゾタチツテトダヂヅデドナニヌネノハヒフヘホバビブベボパピプペポマミムメモヤユヨラリルレロワヰヱヲンッヽ゛゜",
        ##"゠ァアィイゥウェエォオカガキギクグケゲコゴサザシジスズセゼソゾタダチヂッツヅテデトドナニヌネノハバパヒビピフブプヘベペホボポマミムメモャヤュユョヨラリルレロヮワヰヱヲンヴヵヶヷヸヹヺ・ーヽヾヿ",
        ###" !\"#$%&'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\]^_`abcdefghijklmnopqrstuvwxyz{|}~",
        hw.string_from_file("fonts/KAPITAL1.txt"),
        #hw.string_from_file("fonts/utf8.txt"),
        #hw.string_from_file("fonts/jap.txt"),
        #hw.string_from_file("fonts/arabic.txt"),
    ]:
        for distance in range(0, 33, 1):
            print("\n"*4)
            text = hw.string_remove_control_characters(text)
            text = hw.string_make_unique_sorted(text)
            #print("text", hw.dq3_raw(hw.GRAY + text + hw.RESET))
            raw_input = get_string_by_darkness(
                text, 
                "fonts/Everson Mono.ttf", 
                #"fonts/migu-1m-regular.ttf", 
                #"fonts/unifont-14.0.04.ttf", 
                #"fonts/Arial Unicode.ttf", 
                distance=distance,
                make_unique=True,
                make_singular=False
            )   
            ###hw.string_to_file(raw_input, "fonts/KAPITAL1_sorted.txt")
            # raw_input = half_string(raw_input)
            # raw_input = half_string(raw_input)
            # raw_input = half_string(raw_input)
            # raw_input = half_string(raw_input)
            # raw_input = half_string(raw_input)
            # raw_input = half_string(raw_input)


