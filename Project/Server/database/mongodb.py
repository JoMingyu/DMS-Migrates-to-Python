from pymongo import MongoClient

client = MongoClient('localhost', 27017)
db = client.dms

admin_acc = db.admin_acc
student_acc = db.student_acc

afterschool_item = db.afterschool_item
afterschool = db.afterschool
extension = db.extension
goingout = db.goingout
stay = db.stay

bug_report = db.bug_report
recruit = db.recruit

faq = db.faq
notice = db.notice
report_facility = db.report_facility
rule = db.rule

meal = db.meal
