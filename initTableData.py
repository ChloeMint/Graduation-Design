from database import *

with app.app_context():
    # 添加一个账号
    user = User(phone="15715815825", username="芽芽", avatar="/image/yaya.jpg")
    user.set_password("123456")

    db.session.add(user)
    db.session.commit()

    # 添加

    baike1 = Baike(
        plant_name="紫罗兰",
        plant_english_name="Violet",
        introduction="紫罗兰（Matthiola incana (L.) R. "
                     "Br.）是十字花科、紫罗兰属二年生或多年生草本植物，其植株高60"
                     "厘米，布满灰白色的分枝柔毛；茎直立，多分枝；叶片为长圆形至倒披针形或匙形；总状花序顶生和腋生，花多数，较大，花序轴果期伸长，花瓣为类似卵形的紫红、淡红或白色， ["
                     "7]花朵具有芳香、艳丽，花色丰富； [8]种子为深褐色扁平近圆形状，直径约2毫米；花期4-5月",
        care_knowledge="1、土壤：最好用松软、透气、肥沃的土壤。2、光照：平时多晒散光，夏季光照强，必须遮挡处理。3、浇水：生长季勤浇水，保湿在60%-80%之间。4"
                       "、施肥：生长季间勤追施稀释的复合肥液，确保营养足才可更好的开花。5、温度：养护在15-25℃的环境下，夏冬季适当控温。6、注意事项：它有毒，注意摆放位置。",
        area="本属约50种，中国有1种。 [17]原产欧洲南部及地中海沿岸。中国南方大城市中常有引种，北方栽于庭园花坛或温室中。",
        plantCulture='''紫罗兰在古希腊是富饶多产的象征，雅典以它作为徽章旗帜上的标记， [10]是美国罗得岛州的州花， [11]花语是“永恒的美与爱”。 [12]
紫罗兰的花语：永恒的美与爱；质朴，美德，盛夏的清凉。
紫罗兰（蓝色）：警戒，忠诚，我将永远忠诚。
紫罗兰（白色）：让我们抓住幸福的机会吧。
紫罗兰（紫色）：在梦境中爱上你，对我而言你永远那么美。
同时，紫罗兰也是金牛座的幸运花。 [5]
紫罗兰象征：高雅、诚实。 [6]''',
        legendStory="传说中紫罗兰花是“爱情花”，据希腊神话传说故事，管理人们爱与美丽的女神维纳斯，因恋人出远门，依依不舍，晶莹剔透的泪水滴到土壤上，第二年春季居然生出枝芽，结出了一朵朵美丽的花朵来，这就是紫罗兰。"
    )

    baike1.add_image("https://www.huabaike.com/uploads/huatuku/20160527/574806dfcd427.jpg")
    baike1.add_image("https://tse4-mm.cn.bing.net/th/id/OIP-C.yqSwGmP4sC2VzgwYCmosvQHaFC?pid=ImgDet&w=474&h=322&rs=1")
    baike1.add_image("https://tse4-mm.cn.bing.net/th/id/OIP-C.BA-XWKKe54IeX-74eTfBtwHaFM?pid=ImgDet&w=474&h=332&rs=1")

    baike2 = Baike(
        plant_name="郁金香",
        plant_english_name="Tulip",
        introduction="郁金香（Tulipa gesneriana "
                     "L.），是百合科郁金香属草本植物。郁金香鳞茎卵形；鳞茎皮纸质，内面顶端和基部疏生伏毛；叶条状披针形或卵状披针状；花单朵顶生，"
                     "大型而艳丽；花被片红色或杂有白色和黄色，花丝无毛，无花柱，柱头呈鸡冠状；花期4-5月。 [18]郁金香由于花朵（尤其花瓣）近似荷花，又原产于地中海沿岸一带，故名“洋荷花”。",
        care_knowledge="1.光照：郁金香属日中性植物，对日照长短要求不严，喜光，略耐半阴，但光强太低，光合作用减弱，生长不良。2"
                       ".水分：郁金香既不耐干旱也不耐水湿。过湿土壤透气差，容易发生灰霉病，如定植后过分干燥，则会使花芽早期干缩，形成“盲花”。3"
                       ".土壤：喜富含腐殖质的比较肥沃而排水通气良好的沙质壤土，在黏重土壤上生长不良。pH以6.0～7.0为宜。",
        area="郁金香的原种地在中国新疆，新疆郁金香最初由一个传教士从新疆带到土耳其 ["
             "15]，后引进欧洲，17世纪中叶在比利时、荷兰、英国风行。19世纪进入中国上海，20世纪初南京、庐山等地都先后引进应用。中国各地均有引种栽培。",
        plantCulture='''郁金香是荷兰、新西兰、伊朗、土耳其、阿富汗、土库曼斯坦等国的国花。
郁金香——博爱、体贴、高雅、富贵、能干、聪颖、善良。
郁金香（紫）——无尽的爱、最爱。
郁金香（白）——纯洁清高的恋情。
郁金香（粉）——永远的爱。
郁金香（红）——爱的告白、喜悦、热烈的爱意。''',
        legendStory="在荷兰有一个关于郁金香来历的传说：古代有一位美丽的少女，三位勇士同时爱上了她，一个送她一顶皇冠，一个送给她一把宝剑，另一个送了一块金子。 但她对谁都不予钟情，只好向花神祷告。 "
                    "花神深感爱情不能勉强，便将皇冠变为鲜花，宝剑变成绿叶，金子变成茎根，这样合起来便成了一朵郁金香。"
    )

    baike2.add_image("https://bkimg.cdn.bcebos.com/pic/37d3d539b6003af33a87e2c30d7dd15c103853431843?x-bce-process"
                     "=image/format,f_auto/watermark,image_d2F0ZXIvYmFpa2UyNzI,g_7,xp_5,yp_5,P_20/resize,m_lfit,"
                     "limit_1,h_1080")
    baike2.add_image("https://bkimg.cdn.bcebos.com/pic/359b033b5bb5c9ea15ce3040ed6ea1003af33a871543?x-bce-process"
                     "=image/format,f_auto/watermark,image_d2F0ZXIvYmFpa2UyNzI,g_7,xp_5,yp_5,P_20/resize,m_lfit,"
                     "limit_1,h_1080")
    baike2.add_image("https://bkimg.cdn.bcebos.com/pic/023b5bb5c9ea15ce36d3d2aa8e572df33a87e9501443?x-bce-process"
                     "=image/format,f_auto/watermark,image_d2F0ZXIvYmFpa2UyNzI,g_7,xp_5,yp_5,P_20/resize,m_lfit,"
                     "limit_1,h_1080")

    baike3 = Baike(
        plant_name="马蹄莲",
        plant_english_name="calla lily",
        introduction="马蹄莲（Zantedeschia aethiopica (L.) "
                     "Spreng"
                     ".），是木兰纲、天南星科、马蹄莲属多年生粗壮草本。具块茎，并容易分蘖形成丛生植物。叶基生，叶下部具鞘；叶片较厚，绿色，心状"
                     "箭形或箭形，先端锐尖、渐尖或具尾状尖头，基部心形或戟形。喜疏松肥沃、腐殖质丰富的粘壤土",
        care_knowledge=
        '''1.光照温度：马蹄莲喜温暖湿润及稍有遮阴的环境，但花期要阳光充足，否则佛焰苞带绿色，影响品质。须保证每天3—5小时光照，不然叶柄会伸长影响观赏价值。马蹄莲耐寒力不强，10月中旬要移入温室。夏季需要在遮阴情况下，经常喷水降温保湿。 [4]
2.浇水施肥：马蹄莲喜湿润、肥沃土壤，即常说的“大肥大水”，生长期间要多浇水。追肥可用腐熟的豆饼水等液肥与化肥（复合肥或磷酸二铵）轮换施用，每隔2周追施一次。追施液肥时，切忌肥水浇入叶鞘内以免腐烂。以前有人提到：“见花蕾停肥”。经试验对比后，笔者认为见蕾后应增加施肥量，从而保证其花期长，花大而艳，并使花蕾不断，常年开花。 [4]
3.硫酸亚铁的使用：在盆栽马蹄莲中，追施硫酸亚铁是试验的重要环节。追施硫酸亚铁能使马蹄莲叶片变大、变厚、变绿，平滑有光泽，叶柄不易伸长，从而保证叶片美观。同时能促进花蕾形成，延长花期。具体方法是：将硫酸亚铁稀释成2%的溶液，每隔1个月浇施一次，每次要浇透。''',
        area="分布于中国北京、江苏、福建、台湾、四川、云南及秦岭地区栽培供观赏。原产非洲东北部及南部。",
        plantCulture='''花语：博爱，圣洁虔诚，永恒，优雅，高贵，尊贵，希望，高洁，纯洁、纯净的友爱，气质高雅，春风得意，纯洁无瑕的爱。
白色马蹄莲：清雅而美丽，它的花语是“忠贞不渝，永结同心”。
适宜和禁忌:
适宜做新娘的手捧花、小而白的品种宜送年轻朋友，送双数不要送单数。''',
        legendStory="相传有个女孩和男孩邂逅于一个春光明媚的下午，他们的相遇宛如童话故事里的王子与公主的美丽邂逅。女孩单纯、快乐，她的脸上每天都带"
                    "着灿烂的笑容，男孩正直、勇敢，他用心的保护着女孩，给她最大的幸福。他们无忧无虑的生活在小村庄中，一起看花开花落，一起游玩戏耍，"
                    "一起畅想着未来的美好。小小的村庄中每天都能看到他们快乐的身影。然而童话故事终究也只是一个故事而已，他们没能像每一个故事的结局"
                    "一样，王子和公主从此过上幸福的生活。他们生活的村子太小太偏，男孩为了出人头地，实现自己远大的报复，决定去远方闯荡，他骑着骏马"
                    "像雄鹰一样展翅翱翔，奔向他的遥不可及的未来，奔向一个没有女孩的未来。女孩不想成为男孩的负担，因此没有挽留他。在没有男孩的日子"
                    "里，女孩学会了独自生活，学会了思念，她每天都去他们曾经去过的地方，怀念着他们曾经的幸福生活。在一天天的等待与怀念中，女孩一直"
                    "在祈祷着男孩可以找到自己的理想未来，祈祷着男孩可以尽快回来，陪着她看花开花落、细水长流，祈祷着他们的爱可以永恒……最后，女孩变"
                    "成了一种花，一种像女孩一样清新、淡雅的花。这种花，叫马蹄莲。因为女孩最羡慕的是男孩带走的那匹马，她希望自己可以像那匹马一样陪"
                    "男孩一起去每一个地方，走过千山万水。现在也宁愿自己变成马蹄状。她那灿烂的笑，变成了点睛之笔的花蕊，婀娜的身姿变成高挺的茎干，"
                    "绿色的纱裙，化为一片片鲜绿的叶子......"
    )
    baike3.add_image("https://bkimg.cdn.bcebos.com/pic/f703738da9773912b90f44adf2198618377ae2d5?x-bce-process=image"
                     "/format,f_auto/watermark,image_d2F0ZXIvYmFpa2UyNzI,g_7,xp_5,yp_5,P_20/resize,m_lfit,limit_1,"
                     "h_1080")
    baike3.add_image("https://bkimg.cdn.bcebos.com/pic/1b4c510fd9f9d72a6059da6ce37c3f34349b033b0d31")
    baike3.add_image("https://ts1.cn.mm.bing.net/th/id/R-C.82670d844c28f62e42ade06482ce0833?rik=nQAylsaW4M%2btAA&riu"
                     "=http%3a%2f%2fpic1.arkoo.com%2fA25FB809BD3F4C9A9493E5437AB5B318%2fpicture"
                     "%2fo_1cr6kopp3s8kjck1uleg8u1ndhk.jpg&ehk=Zl%2fXJn3Ab15PmOoR%2fmuHdOMiU08xtBkdinIup2pa6f0%3d"
                     "&risl=&pid=ImgRaw&r=0")

    baike4 = Baike(
        plant_name="蝴蝶兰",
        plant_english_name="moth orchid",
        introduction="蝴蝶兰（Phalaenopsis aphrodite Rchb. f.），兰科蝴蝶兰属多年生草本植物， ["
                     "15]茎很短，常被叶鞘所包；叶片稍肉质，上面是绿色，而背面是紫色，呈椭圆形或长圆形，且先端锐尖或钝，具有短而宽的鞘；花色为白色，花瓣呈菱状圆形，且先端圆形，基部收狭呈短爪，具有网状脉。花期4"
                     "—6月。 [16]蝴蝶兰希腊文的原意为“好似蝴蝶般的兰花”，花姿如蝴蝶飞舞而得此名。",
        care_knowledge="蝴蝶兰性喜高温、多湿和半阴环境；不耐寒，怕干旱和强光，忌积水。宜在疏松和排水良好的树皮块、苔藓的土壤种植。生长适温为15-20℃，冬季10℃以下就会停止生长，低于5℃容易死亡。",
        area="蝴蝶兰生于低海拔的热带和亚热带的丛林树干上，分布于中国、泰国、菲律宾、马来西亚、印度尼西亚；在中国分布于台湾（恒春半岛、兰屿、台东）。 [1-2]多生于低海拔的热带和亚热带的丛林树干上。",
        plantCulture='''蝴蝶兰因花朵姿态神似蝴蝶翩翩飞舞而得名，花朵数多而花期长，所以也有“兰花之后”的美誉，象征幸福、长久、丰盛之意，常见颜色有粉红、紫红、橘红、红、白、紫蓝等颜色，并有斑纹、线条变化 [11]。
    蝴蝶兰有着独特的文化象征，人们将它喻为“十分漂亮的公主”，象征女子的清新脱俗和美丽优雅。''',
        legendStory="从前，在一座清秀灵毓的大山里，一个清幽出尘的山谷藏于其中，这个中有一潭清幽的池水。有一次，一只孤独而"
                    "寂寞的蝴蝶翩跹而来，渐渐被这个美丽清幽的空谷小池所吸引，这蝴蝶在心中暗暗赞叹，这般美丽的景色当真是人"
                    "间仙境，在从前的梦里，曾几何时出现过这样的景象，一时间分不清楚是现实还是梦境。蝴蝶不禁赞叹道：“这难"
                    "道不就是我千百年来日夜追寻的地方吗！空谷而绝世！”就在这天晚上，天空划过一颗流星，蝴蝶便许下了自己的"
                    "愿望——但愿在清风荡漾之时，晨露凝结之际，我在那一瞬间化作万千尘埃，而这尘埃落地之时便化作一颗种子，愿"
                    "我可永远守护这座空谷。流星一瞬而过，待春光烂漫的时候，真的就萌发出了幽艳的蝴蝶兰，娇艳美丽的蝴蝶兰开"
                    "满了整个山谷，仿佛千百只翩跹的蝴蝶正在守护着这幽幽空谷。"
    )

    baike4.add_image("https://bkimg.cdn.bcebos.com/pic/c995d143ad4bd11373f025ed77f8b30f4bfbfaedafef?x-bce-process"
                     "=image/format,f_auto/watermark,image_d2F0ZXIvYmFpa2UyNzI,g_7,xp_5,yp_5,P_20/resize,m_lfit,"
                     "limit_1,h_1080")
    baike4.add_image("https://bkimg.cdn.bcebos.com/pic/c9fcc3cec3fdfc03924522596b699094a4c27c1e8881?x-bce-process"
                     "=image/format,f_auto/watermark,image_d2F0ZXIvYmFpa2UyNzI,g_7,xp_5,yp_5,P_20/resize,m_lfit,"
                     "limit_1,h_1080")
    baike4.add_image("https://bkimg.cdn.bcebos.com/pic/b812c8fcc3cec3fdfc03619469dec33f8794a5c28981?x-bce-process"
                     "=image/format,f_auto/watermark,image_d2F0ZXIvYmFpa2UyNzI,g_7,xp_5,yp_5,P_20/resize,m_lfit,"
                     "limit_1,h_1080")

    baike5 = Baike(
        plant_name="报春花",
        plant_english_name="Primula malacoides",
        introduction="报春花（ Primula malacoides "
                     "Franch.）是报春花科报春花属一年生草本植物。叶片在茎基部丛生，有多个浅裂，裂片叶缘呈不整齐锯齿状；花梗上有多轮伞状花序，每轮花序由多朵小花组成 ["
                     "9]，粉红色、淡蓝紫色、或近白色；蒴果球形。花期5—8月，果期8月至翌年6月。 [10]因其开最早，故名“报春花”。",
        care_knowledge="一般用作冷温室盆花的报春花宜用中性土壤栽培。不耐霜冻，花期早。而作为露地花坛布置的欧报春花，则适合生长于阴坡或半阴环境，喜排水良好、富含腐殖质的土壤。",
        area="产中国云南、贵阳和广西西部（隆林）。生长于潮湿旷地、沟边和林缘，海拔1800-3000米。缅甸北部亦有分布。模式标本采自云南大理。",
        plantCulture='''花语：初恋、希望、不悔
    送花对象：朋友、恋人、情人 [6]
    赠花礼仪：用素色的大浅盘装入各种色彩的小盆报春，包上玻璃纸，再将缎带打成十字花结做配饰。
    南宋与范成大、陆游等合称南宋“中兴四大诗人的杨万里，留有词作《嘲报春花》：嫩黄老碧已多时，騃紫痴红略万枝。始有报春三两朵，春深犹自不曾知。''',
        legendStory="传说以前有个年轻的神叫做palarinse，他有一个非常漂亮的未婚妻，两人也十分地相爱。 后来未婚妻身患重病死去离开了他，他非常伤心，茶饭不思，萎靡不振，过了不久也死去了。 "
                    "其它的神对于他的死都纷纷感到惋惜，便将他变成了一种美丽的花，也就是报春花。"
    )
    baike5.add_image("https://bkimg.cdn.bcebos.com/pic/42166d224f4a20a4a63c5b6598529822720ed076?x-bce-process=image"
                     "/format,f_auto/watermark,image_d2F0ZXIvYmFpa2UyNzI,g_7,xp_5,yp_5,P_20/resize,m_lfit,limit_1,"
                     "h_1080")
    baike5.add_image("https://bkimg.cdn.bcebos.com/pic/728da9773912b31bb21ef9e98018367adbb4e1fb?x-bce-process=image"
                     "/format,f_auto/watermark,image_d2F0ZXIvYmFpa2UyNzI,g_7,xp_5,yp_5,P_20/resize,m_lfit,limit_1,"
                     "h_1080")
    baike5.add_image("https://bkimg.cdn.bcebos.com/pic/d0c8a786c9177f3e6709ce0fec872cc79f3df8dcf8d3")

    baike6 = Baike(
        plant_name="吊兰",
        plant_english_name="bracketplant",
        introduction="吊兰（Chlorophytum comosum (Thunb.) Baker），吊兰又称：垂盆草、挂兰、钓兰、兰草、折鹤兰、空气卫士， [1]西欧又叫蜘蛛草或飞机草，原产于南非。",
        care_knowledge="吊兰性喜温暖湿润、半阴的环境。它适应性强，较耐旱，不甚耐寒。不择土壤，在排水良好、疏松肥沃的砂质土壤中生长较佳。对光线的要求不严，一般适宜在中等光线条件下生长，亦耐弱光。生长适温为15"
                       "-25℃，越冬温度为5℃。温度为20-24℃时生长最快，也易抽生匍匐枝。30℃以上停止生长，叶片常常发黄干尖。冬季室温保持12"
                       "℃以上，植株可正常生长，抽叶开花；若温度过低，则生长迟缓或休眠；低于5℃，则易发生寒害。",
        area="原产非洲南部，各地广泛栽培。",
        plantCulture="吊兰的花语是“无奈而又给人希望”。",
        legendStory="吊兰的花语来源于一个传说，说有个妒贤忌才的主考官为了让他的干儿子魁名高中，下决心要捺着那个姓林的才子，在批改林德祥的卷子时恰"
                    "好碰到皇帝微服来访，主考官慌忙之中把卷子藏到案头那盆长得茂盛的兰花中，被相中这盆开得漂亮的皇帝在不经意中看到并得知了实情，结"
                    "局大家都能猜得到，不仅免了他的官职，还把那盆花“赐”给了他。主考官又羞又恼，心生郁闷，不久就死了。从此以后，这种兰花的茎叶就再"
                    "也没有直起来过，且渐渐演变成今天的吊兰，而它的花语也是取其意而来。"
    )
    baike6.add_image("https://bkimg.cdn.bcebos.com/pic/9358d109b3de9c8279793fae6081800a19d843f7?x-bce-process=image"
                     "/format,f_auto/watermark,image_d2F0ZXIvYmFpa2UyNzI,g_7,xp_5,yp_5,P_20/resize,m_lfit,limit_1,"
                     "h_1080")
    baike6.add_image("https://bkimg.cdn.bcebos.com/pic/a9d3fd1f4134970aaa5b2a0c99cad1c8a7865dec?x-bce-process=image"
                     "/format,f_auto/watermark,image_d2F0ZXIvYmFpa2UyNzI,g_7,xp_5,yp_5,P_20/resize,m_lfit,limit_1,"
                     "h_1080")
    baike6.add_image("https://bkimg.cdn.bcebos.com/pic/060828381f30e924b94ea71240086e061d95f72e?x-bce-process=image"
                     "/format,f_auto/watermark,image_d2F0ZXIvYmFpa2UyNzI,g_7,xp_5,yp_5,P_20/resize,m_lfit,limit_1,"
                     "h_1080")

    baike7 = Baike(
        plant_name="风信子",
        plant_english_name="hyacinth",
        introduction="风信子（Hyacinthus orientalis L. Sp. "
                     "Pl.），是天门冬科风信子属的多年生草本植物，学名得自希腊神话中受太阳神阿波罗宠眷、并被其所掷铁饼误伤而死的美少年雅辛托斯（Hyacinth）。 "
                     "根为球根；鳞茎呈卵形，有膜质外皮，皮膜颜色与花色成正相关，未开花时形如大蒜；叶呈狭披针形，肉质，肥厚，绿色有光；花据其花色可大致分为蓝色、"
                     "粉红色、白色、鹅黄、紫色、黄色、绯红色、红色等八个品系，花期为早春，原种为浅紫色，有芳香气味",
        care_knowledge="风信子习性喜阳、耐寒，适合生长在凉爽湿润的环境和疏松、肥沃的砂质土中，忌积水。喜冬季温暖湿润、夏季凉爽稍干燥、阳光充足或半阴的环境。喜肥，宜肥沃、排水良好的沙壤土。地植、盆栽、水养均可。",
        area="风信子原产于欧洲南部地中海沿岸及小亚细亚一带、荷兰，如今世界各地都有栽培。野生种生于西亚及中亚的海拔2600米以上的石灰岩地区。",
        plantCulture="风信子花语：胜利、竞技、喜悦、爱意、幸福、浓情、倾慕、顽固、生命、得意、永远的怀念。",
        legendStory="希腊神话中受太阳神阿波罗（Απλλων）宠眷、并被其所掷铁饼误伤而死的美少年雅辛托斯（κινθο），是由于西风风神泽费奴斯（Zephyrus"
                    "）用计害死。在雅辛托斯的血泊中，长出了一种美丽的花，阿波罗便以少年的名字命名这种花——风信子υκινθο（Hyacinthus orientalis）。"
    )
    baike7.add_image("https://bkimg.cdn.bcebos.com/pic/a50f4bfbfbedab64034f1bcb8f60b8c379310a55b038?x-bce-process"
                     "=image/format,f_auto/watermark,image_d2F0ZXIvYmFpa2UyNzI,g_7,xp_5,yp_5,P_20/resize,m_lfit,"
                     "limit_1,h_1080")
    baike7.add_image("https://bkimg.cdn.bcebos.com/pic/962bd40735fae6cd7b890c2e37e4182442a7d933a17f?x-bce-process"
                     "=image/format,f_auto/watermark,image_d2F0ZXIvYmFpa2UyNzI,g_7,xp_5,yp_5,P_20/resize,m_lfit,"
                     "limit_1,h_1080")
    baike7.add_image("https://bkimg.cdn.bcebos.com/pic/b8014a90f603738da9778c6d8b4ca751f8198618467e?x-bce-process"
                     "=image/format,f_auto/watermark,image_d2F0ZXIvYmFpa2UyNzI,g_7,xp_5,yp_5,P_20/resize,m_lfit,"
                     "limit_1,h_1080")

    baike8 = Baike(plant_name="夹竹桃", plant_english_name="Oleander",
                   introduction="夹竹桃（Nerium oleanderL.），夹竹桃属常绿直立大灌木。枝条灰绿色，含水液；叶面深绿，无毛，叶背" "浅绿色，有多数坑洼的小点；最中央的花最先开放，着花数朵，雄蕊的下部短，被长柔毛；种子长圆形，底部较"
                                "窄，顶端钝、褐色。夹竹桃花期为六月到十月。 [4]因为花似桃、茎似竹，才得名夹竹桃。",
                   care_knowledge="喜温暖湿润的气候，耐寒力不强，在中国长江流域以南地区可以露地栽植，但在南京有时枝叶冻枯，小苗甚"
                                  "至冻死。在北方只能盆栽观赏，室内越冬，白花品种比红花品种耐寒力稍强：夹竹桃不耐水湿，要求选择高" "燥和排水良好的地方栽植，喜光好肥，也能适应较阴的环境，但庇荫处栽植花少色淡。萌蘖力强，树体受害" "后容易恢复。",
                   area="夹竹桃原产于印度、伊朗和尼泊尔， [1]中国各省区有栽培，尤以中国南方为多，常在公园、风景区、道路旁或河旁、湖旁周围栽培；长江以北栽培者须在温室越冬。野生于伊朗、印度、尼泊尔；现广植于世界热带地区。",
                   plantCulture="桃色夹竹桃：咒骂，注意危险；黄色夹竹桃的花语：深刻的友情。",
                   legendStory="传说中有个美丽的女孩桃，爱上了一个倔强的男孩竹，但是却受到了桃家人的反对将竹活活打死，桃伤心欲绝随着"
                               "爱人一起，殉情自杀了，两人来到天堂后，上帝为之感动，说能够满足他们一个要求，桃说她一生最爱的就是美丽" "的桃花，而竹却倔强的想要保留竹一样的坚韧，从此，世上就多了一种——夹竹桃，开着桃花一样的花有着竹一样的" "叶子。")

    baike8.add_image("https://bkimg.cdn.bcebos.com/pic/0e2442a7d933c895a19ad788d11373f083020058?x-bce-process=image"
                     "/format,f_auto/watermark,image_d2F0ZXIvYmFpa2UyNzI,g_7,xp_5,yp_5,P_20/resize,m_lfit,limit_1,"
                     "h_1080")
    baike8.add_image("https://bkimg.cdn.bcebos.com/pic/6a600c338744ebf8cb952bccd9f9d72a6159a759?x-bce-process=image"
                     "/format,f_auto/watermark,image_d2F0ZXIvYmFpa2UyNzI,g_7,xp_5,yp_5,P_20/resize,m_lfit,limit_1,"
                     "h_1080")
    baike8.add_image("https://bkimg.cdn.bcebos.com/pic/d043ad4bd11373f0f6d8206ca40f4bfbfaed0459?x-bce-process=image"
                     "/format,f_auto/watermark,image_d2F0ZXIvYmFpa2UyNzI,g_7,xp_5,yp_5,P_20/resize,m_lfit,limit_1,"
                     "h_1080")

    db.session.add_all([baike1, baike2, baike3, baike4, baike5, baike6, baike7, baike8])
    db.session.commit()

    dongtai1 = DongTai(
        user_id=1,
        like_num=100,
        article_text="article1"
    )

    dongtai1.add_image("https://bkimg.cdn.bcebos.com/pic/8435e5dde71190ef661cdd2cce1b9d16fcfa6059?x-bce-process=image"
                       "/format,f_auto/watermark,image_d2F0ZXIvYmFpa2UyNzI,g_7,xp_5,yp_5,P_20/resize,m_lfit,limit_1,"
                       "h_1080")

    comment1 = Comment(
        article_id=1,
        comment_user_id=1,
        comment_text="comment1"
    )

    note1 = Note(
        user_id=1,
        title="note1",
        content="note1 and content1"
    )

    if __name__ == "__main__":
        db.session.add_all([dongtai1, comment1, note1])
        db.session.commit()
