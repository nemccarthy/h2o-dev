import unittest, random, sys, time
sys.path.extend(['.','..','../..','py'])
import h2o, h2o_browse as h2b, h2o_exec as h2e, h2o_import as h2i

initList = [

        # '(= !keys (ls))', # works
        # '(= !x #1)', # works
        # '(= !x (sum ([ $r1 "null" #0) $TRUE))', # works
        # '(= !x (sum ([ r1 "null" (: #0 #0)) $TRUE))', # bad r1

        # '(= !x (xorsum ([ $r1 "null" #0) $TRUE))', # works

        # 'a',  # AAIOBE
        # 'x', # AAIOBE
        # 'c', # AAIOBE
        # 'c(1)', # says 'c(1' is unimplemented

        # '(= #1)', # AAIOBE
        # '(= !x #1)', # works
        # 'x=c(1.3,0,1,2,3,4,5)', # says 'x=c(1.3,0,1,2,3,4,5' is unimplemented
        # 'x=c(1.3',  # AAIOBE
        # '()',  # Unimplemented on token ''
        # '(x)', # unimplemented on x
        # '(= !x)', # AAIOBE
        # '(= !x ())', # unimplemented
        # '(= !x #1)', # works
        # '(= !x #1 #2)',  # works, answer is 1?
        # '(= !x (cbind (#1 #2) $TRUE))',  # ClassCast exception
        # '(= !x (cbind (#1 #2)))',  # ClassCast exception
        # '(= !x (cbind (#1)))',  # ClassCast exception
        # '(= !x (cbind #1))',  # ClassCast exception
        # '(= !x (seq (#1, #2)) )',  # number format exception
        # '(= !x (seq (#1, #2)) )',  # bad
        # '(= !x (seq #1, #2) )',  # bad

        # '(= !x (seq (#1) )',  # bad
        # '(= !x #1; = !x #2)', # no error but why answer is 1?
        # '(= !x #1) (=!x #2)', # no error but why answer is 1?
        # '{(= !x #1); (=!y $x)', # AAIOBE
        # '{(= !x #1)', # AAIOBE
        # '({(= !x #1); (= !y #1))', # AAIOBE
        # '(1)',
        # '((1))',
        # '(((1)))',

        '(#(1))', # why isn't this illegal?

        '(#1)',
        '((#1))',
        '(((#1)))',

        '(= !x #1)',
        '((= !x #1))',
        '(((= !x #1)))',

        # complains
        # '(= !x (#1 #2))',
        # '((= !x (#1 #2)))',
        # '(((= !x (#1 #2))))',

        # okay. not okay if comma separated. seems wrong
        '(= !x (+ #1 #2))',
        '((= !x (+ #1 #2)))',
        '(((= !x (+ #1 #2))))',

        # complains
        # '(= !x (+ #1 #2 #4))',
        # '((= !x (+ #1 #2 #4)))',
        # '(((= !x (+ #1 #2 #4))))',

        # okay. 
        '(= !x + #1 #2)',
        '((= !x + #1 #2))',
        '(((= !x + #1 #2)))',

        # '(= x + #1 #2)', # fails

        # parens on binary operators
        '(= !x + #1 + #1 (+ #1 #1))',
        '= !x + #1 + #1 (+ #1 #1)',
        '= !x N #1 N #1 (N #1 #1)',
        '= !x n #1 n #1 (n #1 #1)',
        '= !x L #1 L #1 (L #1 #1)',
        '= !x l #1 l #1 (l #1 #1)',
        '= !x G #1 G #1 (G #1 #1)',
        '= !x g #1 g #1 (g #1 #1)',

        '= !x * #1 * #1 (* #1 #1)',
        '= !x - #1 - #1 (- #1 #1)',
        '= !x ^ #1 ^ #1 (^ #1 #1)',
        '= !x / #1 / #1 (/ #1 #1)',
        '= !x ** #1 ** #1 (** #1 #1)',
        '= !x % #1 % #1 (% #1 #1)',
        # '= !x %/% #1 %/% #1 %/% #1 #1', # unimplemented
        # '= !x %% #1 %% #1 %% #1 #1', # unimplemented

        # '(= !x + _#1 + _#1 + _#1 _#1)', # unimplemented
        '= !x _ + #1 + #1 (+ #1 _ #1)',
        '= !x _ N #1 N #1 (N #1 _ #1)',
        '= !x _ n #1 n #1 (n #1 _ #1)',
        '= !x _ L #1 L #1 (L #1 _ #1)',
        '= !x _ l #1 l #1 (l #1 _ #1)',
        '= !x _ G #1 G #1 (G #1 _ #1)',
        '= !x _ g #1 g #1 (g #1 _ #1)',

        '= !x _ * #1 * #1 (* #1 _ #1)',
        '= !x _ - #1 - #1 (- #1 _ #1)',
        '= !x _ ^ #1 ^ #1 (^ #1 _ #1)',
        '= !x _ / #1 / #1 (/ #1 _ #1)',
        '= !x _ ** #1 ** #1 (** #1 _ #1)',
        '= !x _ % #1 % #1 (% #1 _ #1)',


        # can't have space between ( and function
        '= !x1 (sum ([ $r1 "null" #0) $TRUE)',
        '= !x2 (sum ([ $r1 "null" #0) $TRUE)',
        '= !x2a (sum ([ $r1 "null" #0) $TRUE )',

        # can't have space after (
        '= !x3 (sum ([ $r1 "null" #0) $TRUE )',
        '= !x3a (sum ([ $r1 "null" #0) $TRUE )',
        '= !x3b (sum ([ $r1 "null" #0 ) $TRUE )',
        '= !x4 (sum ([ $r1 " null " #0 ) $TRUE )',

        # can't have space after (
        '(= !x3 (sum ([ $r1 "null" #0) $TRUE ))',
        '(= !x3a (sum ([ $r1 "null" #0) $TRUE ) )',
        '(= !x3b (sum ([ $r1 "null" #0 ) $TRUE )  )',
        '((= !x4 (sum ([ $r1 " null " #0 ) $TRUE )))',
        # '= !x (sum $r1 )'
        # '(= !x (xorsum ([ $r1 "null" #0) $TRUE))', # works

        
        # 'cave=c(1.3,0,1,2,3,4,5)',
        # 'ma=c(2.3,0,1,2,3,4,5)',
        # 'r2.hex=c(3.3,0,1,2,3,4,5)',
        # 'r3.hex=c(4.3,0,1,2,3,4,5)',
        # 'r4.hex=c(5.3,0,1,2,3,4,5)',
        # 'r.hex=i.hex',
        ]

exprList = [
    "round(r.hex[,1],0)",
    "round(r.hex[,1],1)",
    "round(r.hex[,1],2)",
    # "signif(r.hex[,1],-1)",
    # "signif(r.hex[,1],0)",
    "signif(r.hex[,1],1)",
    "signif(r.hex[,1],2)",
    "signif(r.hex[,1],22)",
    "trunc(r.hex[,1])",
    "trunc(r.hex[,1])",
    "trunc(r.hex[,1])",
    "trunc(r.hex[,1])",

    ## Compute row and column sums for a matrix:
    # 'x <- cbind(x1 = 3, x2 = c(4:1, 2:5))',

    # 'dimnames(x)[[1]] <- letters[1:8]',
    # 'apply(x, 2, mean, trim = .2)',
    'apply(x, 2, mean)',
    'col.sums <- apply(x, 2, sum)',
    'row.sums <- apply(x, 1, sum)',
    # 'rbind(cbind(x, Rtot = row.sums), Ctot = c(col.sums, sum(col.sums)))',
    # 'stopifnot( apply(x, 2, is.vector))',
    ## Sort the columns of a matrix
    # 'apply(x, 2, sort)',
    ##- function with extra args:
    # 'cave <- function(x, c1, c2) c(mean(x[c1]), mean(x[c2]))',
    # 'apply(x, 1, cave,  c1 = "x1", c2 = c("x1","x2"))',
    # 'ma <- matrix(c(1:4, 1, 6:8), nrow = 2)',
    'ma',
    # fails unimplemented
    # 'apply(ma, 1, table)',  #--> a list of length 2
    # 'apply(ma, 1, stats::quantile)', # 5 x n matrix with rownames
    #'stopifnot(dim(ma) == dim(apply(ma, 1:2, sum)))',
    ## Example with different lengths for each call
    # 'z <- array(1:24, dim = 2:4)',
    # 'zseq <- apply(z, 1:2, function(x) seq_len(max(x)))',
    # 'zseq',        ## a 2 x 3 matrix
    # 'typeof(zseq)', ## list
    # 'dim(zseq)', ## 2 3
    # zseq[1,]',
    # 'apply(z, 3, function(x) seq_len(max(x)))',
    # a list without a dim attribute
]


class Basic(unittest.TestCase):
    def tearDown(self):
        h2o.check_sandbox_for_errors()

    @classmethod
    def setUpClass(cls):
        global SEED
        SEED = h2o.setup_random_seed()
        h2o.init(1)

    @classmethod
    def tearDownClass(cls):
        h2o.tear_down_cloud()

    def test_rapids_basic(self):
        bucket = 'smalldata'
        csvPathname = 'iris/iris_wheader.csv'
        hexKey = 'r1'
        parseResult = h2i.import_parse(bucket=bucket, path=csvPathname, schema='put', hex_key=hexKey)

        for execExpr in initList:
            h2e.exec_expr(h2o.nodes[0], execExpr, resultKey=None, timeoutSecs=4)

        # for execExpr in exprList:
        #     h2e.exec_expr(execExpr=execExpr, resultKey=None, timeoutSecs=10)

        h2o.check_sandbox_for_errors()


if __name__ == '__main__':
    h2o.unit_main()