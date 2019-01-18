import schemedit as sce

if sce.surrounding(4, 6) == \
   [ [3, 6, 0, 3, 6, 0]
   , [4, 6, 0, 5, 6, 0]
   , [4, 5, 1, 4, 5, 1]
   , [4, 6, 1, 4, 7, 1] ]:
  print("[OK]", end="")
else:
  print("[ER]", end="")
print(" surrounding")

def radix(rdx, i):
  acc = []
  while 0 < i:
    acc.append(i % rdx)
    i = i // rdx
  return acc

def radix_inv(rdx, a):
  acc = 0
  for i in range(len(a)-1, -1, -1):
    acc = acc*rdx + a[i]
  return acc

def radix2_inv(a):
  return radix_inv(2, a)

def decode1(n, str):
  acc = []
  for c in str:
    i = 0 if c == ' ' else int(c, 16)
    a = radix(2, i) + [0] * n
    acc.append(a[0:n])
  return acc

def decode(n, strs):
  return [decode1(n, str) for str in strs]

def mapd(d, f, s):
  if d <= 0:
    return f(s)
  else:
    return [mapd(d-1, f, x) for x in s]

test_pattern = \
["    1     ", "          ",
 "    1     ", "          ",
 "  223222  ", "  222222  ",
 "    1     ", "          ",
 "    1     ", "          ",
 "    1     ", "          ",
 "  227222  ", "          ",
 "    1     ", "          ",
 "    1     ", "          ",
 "    1     ", "          "]
tested   = test_pattern[0::2]
expected = test_pattern[1::2]
val      = sce.trace(decode(3, tested), 2, 3, 1)
for line in mapd(2, radix2_inv, val):
  print(line)
#if sce.trace(decode(3, tested), 2, 3, 1) == decode(2, expected):
if val == decode(2, expected):
  print("[OK]", end="")
else:
  print("[ER]", end="")
print(" trace")

#(deftest test-beam
#  (let [test-pattern
#        ["0000000000"
#         "0032227200"
#         "0010001010"
#         "0010001010"
#         "0000000000"
#         "0000000000"]]
#    (is (= (smp/beam (decode 3 test-pattern) [1 4] 1)
#           [[1 2] [1 6]]))
#    (is (= (smp/beam (decode 3 test-pattern) [1 2] 0)
#           [[1 2] [4 2]]))))

#(deftest test-drawable?
#  (let [test-pattern
#        ["0000000000" "0000000000"
#         "0032227200" "0032227200"
#         "0010001010" "0010001010"
#         "0010001010" "0010001010"
#         "0000000000" "0000000000"
#         "0032227200" "0000000000"
#         "0010001010" "0000000000"
#         "0010001010" "0000000000"
#         "0000000000" "0000000000"]
#        [field traced] (->> test-pattern
#                            (map (partial decode1 3))
#                            (partition 2)
#                            (apply map vector))]
#    (is      (smp/drawable? 4 2 1 traced field) )
#    (is      (smp/drawable? 6 2 1 traced field) )
#    (is (not (smp/drawable? 5 3 1 traced field)))
#    ))

#(deftest test-add-dot
#  (let [test-pattern
#        ["0000000000" "0000000000" "0000000000"
#         "0000000000" "0000000000" "0000000000"
#         "0022232220" "0022272220" "0022272220"
#         "0000010000" "0000010000" "0000010000"
#         "0002210000" "0002210000" "0002250000"
#         "0000010000" "0000010000" "0000010000"
#         "0032232200" "0032232200" "0032232200"
#         "0010010000" "0010010000" "0010010000"
#         "0022200000" "0022200000" "0022200000"
#         "0000000000" "0000000000" "0000000000"]
#        [field ex1 ex2] (->> test-pattern
#                             (map (partial decode1 3))
#                             (partition 3)
#                             (apply map vector))]
#    (is (= (smp/add-dot [2 2] 8 1 field field) ex1  ))
#    (is (= (smp/add-dot [2 5] 8 0 field field) ex2  ))
#    ;(clojure.pprint/pprint
#    ; (mapd 2 (comp (partial reduce (fn [acc x] (+ (* acc 2) x)))
#    ;               reverse)
#    ;         (smp/add-dot [2 5] 8 0 field field)))
#    (is (= (smp/add-dot [7 2] 8 1 field field) field))
#    ))

#(deftest test-draw-net-1
#  (let [test-pattern 
#        ["0000000000" "0000000000" "0000000000"
#         "0000000000" "0022222200" "0000000000"
#         "0000000000" "0000000000" "0000100000"
#         "0000000000" "0000000000" "0000100000"
#         "0000000000" "0000000000" "0000100000"
#         "0000000000" "0000000000" "0000100000"
#         "0000000000" "0000000000" "0000100000"
#         "0000000000" "0000000000" "0000000000"
#         "0000000000" "0000000000" "0000000000"
#         "0000000000" "0000000000" "0000000000"]
#        [field ex1 ex2] (->> test-pattern
#                             (map (partial decode1 3))
#                             (partition 3)
#                             (apply map vector))]
#    (is (= (smp/draw-net-1 [1 2] 8 1 field) ex1))
#    (is (= (smp/draw-net-1 [2 4] 7 0 field) ex2))))

#(deftest test-stumble
#  (let [test-pattern
#        ["0000000000" "0000000000" "0000000000" "0000000000"
#         "0000000000" "0000000000" "0000000000" "0000001000"
#         "0000022200" "0000000000" "0000022200" "0000023200"
#         "0000000000" "0000000000" "0000000000" "0000001000"
#         "0000022200" "0000022200" "0022222200" "0000023200"
#         "0000000000" "0000000000" "0000000000" "0000001000"
#         "0000022200" "0000022200" "0000022200" "0000022200"
#         "0000000000" "0000000000" "0000000000" "0000000000"
#         "0000000000" "0000000000" "0000000000" "0000000000"
#         "0000000000" "0000000000" "0000000000" "0000000000"]
#        [field traced ex1 ex2] (as-> test-pattern t
#                                     (map (partial decode1 3) t)
#                                     (partition 4 t)
#                                     (apply map vector t))]
#    (is (= (nth (smp/stumble [2 2] 5 1 traced field) 1) nil))
#    (is (= (nth (smp/stumble [4 2] 6 1 traced field) 1) ex1))
#    (is (= (nth (smp/stumble [1 5] 6 0 traced field) 1) nil))
#    (is (= (nth (smp/stumble [1 6] 6 0 traced field) 1) ex2))))

#(deftest test-reach
#  (let [test-pattern
#        ["0000000000" "0000000000" "0000000000" "0000000000"
#         "0010000000" "0010000000" "0010000000" "0010000000"
#         "0010000000" "0010000000" "0010000000" "0010000000"
#         "0010002200" "0010000000" "0010002200" "0010002200"
#         "0010000000" "0010000000" "0010000000" "0010000000"
#         "0010000000" "0010000000" "0010000000" "0010000000"
#         "0000000000" "0000000000" "0000000000" "0010000000"
#         "0000000000" "0000000000" "0000000000" "0000000000"
#         "0000000000" "0000000000" "0000000000" "0000000000"
#         "0000000000" "0000000000" "0000000000" "0000000000"]
#        [field traced ex1 ex2] (as-> test-pattern t
#                                     (map (partial decode1 3) t)
#                                     (partition 4 t)
#                                     (apply map vector t))]
#    (is (= (nth (smp/reach [3 2] :u traced field) 1) ex1))
#    (is (= (nth (smp/reach [7 2] :u traced field) 1) ex2))
#    (is (= (nth (smp/reach [3 8] :l traced field) 1) nil))
#    (is (= (nth (smp/reach [3 8] :r traced field) 1) nil))))

#(deftest test-debridge
#  (let [test-pattern
#        ["0000000000" "0000000000" "0000000000" "0000000000"
#         "0032221000" "0010001000" "0032220000" "0032221000"
#         "0010001000" "0010001000" "0010000000" "0010001000"
#         "0010001000" "0010001000" "0010000000" "0010001000"
#         "0072225000" "0072225000" "0072221000" "0010001000"
#         "0010001000" "0010001000" "0010001000" "0010001000"
#         "0000001000" "0000001000" "0000001000" "0000001000"
#         "0000001000" "0000001000" "0000001000" "0000001000"
#         "0000220000" "0000220000" "0000220000" "0000220000"
#         "0000000000" "0000000000" "0000000000" "0000000000"]
#        [field ex1 ex2 ex3] (as-> test-pattern t
#                                  (map (partial decode1 3) t)
#                                  (partition 4 t)
#                                  (apply map vector t))]
#    (is (= (smp/debridge [1 2] 6 1 field) ex1))
#    (is (= (smp/debridge [1 6] 4 0 field) ex2))
#    (is (= (smp/debridge [4 2] 6 1 field) ex3))))

#(deftest test-shave
#  (let [test-pattern
#        ["0000000000" "0000000000" "0000000000" "0000000000"
#         "0010001000" "0000001000" "0010000000" "0010001000"
#         "0010001000" "0000001000" "0010000000" "0010001000"
#         "0010001000" "0000001000" "0010000000" "0010001000"
#         "0072225000" "0032225000" "0072221000" "0072225000"
#         "0010001000" "0010001000" "0010001000" "0010001000"
#         "0000001000" "0000001000" "0000001000" "0000001000"
#         "0000001000" "0000001000" "0000001000" "0000001000"
#         "0000220000" "0000220000" "0000220000" "0000000000"
#         "0000000000" "0000000000" "0000000000" "0000000000"]
#        [field ex1 ex2 ex3] (as-> test-pattern t
#                                  (map (partial decode1 3) t)
#                                  (partition 4 t)
#                                  (apply map vector t))]
#    (is (= (smp/shave [1 2] 9 :d field) ex1))
#    (is (= (smp/shave [1 6] 9 :d field) ex2))
#    (is (= (smp/shave [8 4] 9 :r field) ex3))))

#(deftest test-move-x
#  (let [test-pattern
#        ["0000000000" "0000000000"
#         "0032221000" "0000001000"
#         "0010001000" "0000001000"
#         "0010001000" "0000001000"
#         "0022223220" "0000007220"
#         "0000001000" "0000001000"
#         "0000001000" "0000001000"
#         "0000001000" "0000001000"
#         "0000000000" "0000000000"
#         "0000000000" "0000000000"]
#        [field ex1] (as-> test-pattern t
#                          (map (partial decode1 3) t)
#                          (partition 2 t)
#                          (apply map vector t))]
#    (is (= (smp/move-x field [2 2] 6) ex1))))

#(deftest test-move-y
#  (let [test-pattern
#        ["0000000000" "0000000000"
#         "0032221000" "0000000000"
#         "0010001000" "0000000000"
#         "0010001000" "0000000000"
#         "0022223220" "0022227220"
#         "0000001000" "0000001000"
#         "0000001000" "0000001000"
#         "0000001000" "0000001000"
#         "0000000000" "0000000000"
#         "0000000000" "0000000000"]
#        [field ex1] (as-> test-pattern t
#                          (map (partial decode1 3) t)
#                          (partition 2 t)
#                          (apply map vector t))]
#    (is (= (smp/move-y field [1 4] 4) ex1))))
