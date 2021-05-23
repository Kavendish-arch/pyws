# ItemCF 协同过滤算法
from datetime import datetime
from operator import itemgetter
import tool as tool


class ItemCF(object):
    def __init__(self):
        self.trainSet = {}
        self.testSet = {}
        self.trainSet_len = 0
        self.testSet_len = 0

        self.movie_sim_matrix = {}
        self.movie_popular = {}

        self.evaluates = {}

        # 推荐相似电影：
        self.n_sim_movie = 20
        self.n_rec_movie = 20

        self.calc_sim = tool.jacard


    def initData(self, data_path):
        # read file
        self.trainSet, self.testSet = tool.get_dataset(data_path)


    def create_movie_movie_matrix(self):
        """
        统计电影的播放次数，movie_movie 矩阵
        self.movie_popular

        建立 movie movie 矩阵
        self.movie_sim_matrix
        """

        self.movie_popular, self.movie_sim_matrix \
            = tool.build_movie_matrix(self.trainSet)


    def calc_movie_sim(self):
        """
        # 计算电影之间的相似度
        """
        self.movie_sim_matrix = self.calc_sim(
            self.movie_popular, self.movie_sim_matrix)


    # 针对目标用户U，找到K部相似的电影，并推荐其N部电影，
    # 用户未产生过行为的物品
    def recommend(self, user_id):
        # 推荐项目的个数, 推荐范围
        K,N = self.n_sim_movie, self.n_rec_movie
        # 用户user对物品的偏好值
        # 用户user产生过行为的物品，与物品item按相似度从大到小排列，取与物品item相似度最大的k个商品
        # 验证是否有用户的历史记录
        self.rank = {}
        try:
            watched_movies = self.trainSet[user_id]
        except KeyError:
            print(user_id + " is not exits")
            return

        for movie, rating in watched_movies.items():
            # 遍历与物品item最相似的前k个产品，获得这些物品及相似分数
            for related_movie, w in \
                    sorted(self.movie_sim_matrix[movie].items(),
                           key=itemgetter(1), reverse=True)[:K]:
                # 若该物品为当前物品，跳过
                if related_movie in watched_movies:
                    continue
                # 计算用户user对related_movie的偏好值，初始化该值为0
                self.rank.setdefault(related_movie, 0)
                
                # 通过与其相似物品对物品related_movie的偏好值相乘并相加。
                # 排名的依据—— > 推荐电影与该已看电影的相似度(累计) * 用户对已看电影的评分
                self.rank[related_movie] += w * float(rating)
        return sorted(self.rank.items(), key=itemgetter(1), reverse=True)[:N]

    # 产生推荐并通过准确率、召回率和覆盖率进行评估
    def evaluate(self):
        print('算法评价过程......')
        N = self.n_rec_movie
        # 准确率和召回率
        # 总命中数
        all_hit = 0
        # 总推荐数
        rec_count = 0
        # 总结果数
        test_count = 0
        # 每个用户的 评价
        # 覆盖率
        all_rec_movies = set()
        confusion_matrix = {}
        # i, user：user_id
        for i, user in enumerate(self.trainSet):
            hit = 0
            # 读取测试集
            test_movies = self.testSet.get(user, {})
            # 推荐集合
            rec_movies = self.recommend(user)
            user_evaluate = {}
            user_evaluate.setdefault('train_len', len(self.trainSet.get(user)))
            user_evaluate.setdefault('test_len', len(test_movies))
            user_evaluate.setdefault('rec_len', len(rec_movies))

            
            confusion = {}
            for movie, w in rec_movies:
                if movie in test_movies:
                    # 推荐结果命中
                    hit += 1
                # 所有推荐的电影
                all_rec_movies.add(movie)
            user_evaluate.setdefault('hit', hit)
            all_hit += hit
            rec_count += N

            confusion.setdefault('tp', hit)
            confusion.setdefault('fp', N - hit)
            confusion.setdefault('tn', len(test_movies) - hit)
            confusion.setdefault('fn', len(self.movie_popular) -
                                 len(self.trainSet.get(user)))
            # 每个用户的 f1 score
            # user_precision = 0 if len(rec_movies) == 0 else hit / len(rec_movies)
            # user_recall = 0 if len(test_movies) == 0 else hit / len(test_movies)
            #
            # f1_score = -1 if user_recall + user_precision == 0\
            #     else 2 * user_precision * user_recall \
            #                / (user_precision + user_recall)
            #
            # user_evaluate.setdefault('precision', user_precision)
            # user_evaluate.setdefault('recall', user_recall)
            # user_evaluate.setdefault('f1_score', f1_score)
            self.evaluates.setdefault(user, user_evaluate)
            confusion_matrix.setdefault(user, confusion)
            test_count += len(test_movies)

        precision = hit / (1.0 * rec_count)
        recall = hit / (1.0 * test_count)
        coverage = len(all_rec_movies) / (1.0 * len(self.movie_popular))
        print('命中=%.4f\t推荐总数=%.4f\t结果集总数=%.4f' % (
            all_hit, rec_count, test_count))
        print('总命中率=%.10f\t总召回率=%.10f\t推荐电影占比=%.10f' % (
            precision, recall, coverage))


if __name__ == "__main__":
    """
        
    """
    base = ItemCF()
    base.calc_sim = tool.jacard

    path = 'ratings.csv'

    # read_file
    base.initData(path)

    a = datetime.now()
    base.create_movie_movie_matrix()
    base.calc_movie_sim_jacard()
    b = datetime.now()
    base.evaluates.setdefault("method_calc_movie_sim_jacard",
                              (b - a).seconds)

    a = datetime.now()
    base.evaluate()
    b = datetime.now()
    print("evaluate ", (b - a).seconds)
    base.evaluates.setdefault("method_evaluate", (b - a).seconds)

    ii = 0
    tool.save_as_csv(base, '..\\csv\\itemCF_1_3.csv')

    tool.save_as_shelve(base.evaluates.keys(),
                        base.evaluates, '..\\data\\itemCF_1_3.data')
