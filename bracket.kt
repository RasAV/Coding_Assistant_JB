fun brackets(str: String) : String{
    // function that puts brackets in correct order

    //short word case
    if (str.length < 3) {
        return str
    }

    //general case
    var str2 = "" + str[0]
    val n = str.length

    val mid1 : Int = n / 2
    val mid2 : Int = (n + 1) / 2

    for (i in 1..mid1-1) {
        str2 += "(" + str[i]
    }

    if (mid2 > mid1) {
        str2 += "(" + str.substring(mid1, mid2) + ")"
    }

    for (i in mid2..n-2) {
        str2 += str[i] + ")"
    }
    str2 += str[n-1]
    return  str2
}



fun main() {
    val str = readLine().toString()
    println(brackets(str))
}
