/-
Author: Chris Su
Date:                Oct 12, 2025
Program Name:        Puzzle solution for math.inc

LinkedIn:            linkedin.com/in/chrissuu
GitHub:              github.com/chrissuu
Personal Website:    chrissuu.com
Email:               chrissu@andrew.cmu.edu
-/

/-
math.inc

Suppose that today is June 1, 2025. We call a date "square" if all of its components
(day, month, and year) are perfect squares. I was born in the last millennium,
and my next birthday (relative to that date) will be the last square date in my
life. If you sum the square roots of the components of that upcoming square birthday
(day, month, year), you obtain my age on June 1, 2025. My mother would have been born
on a square date if the month were a square number; in reality it is not a square date,
but both the month and day are perfect cubes. When was I born, and when was my mother born?
-/

import Mathlib.Tactic
open Nat
open List

/-
Date Definition & Helpers
-/
structure Date where
  month : Nat
  day : Nat
  year : Nat
  deriving Repr, BEq

def is_square (n : Nat) : Bool :=
  let k := sqrt n
  n == k * k

def nat_root (n k : Nat) : Option Nat :=
  if k = 0 then none
  else if n = 0 then some 0
  else
    (List.range (n + 1)).find? (fun x => x^k = n)

def is_cubic (n : Nat) : Bool :=
  if n = 0 then false
  else
    let root_candidate := nat_root n 3
    match root_candidate with
    | some root => root * root * root == n
    | _ => false

def is_square_date (date : Date) : Bool :=
  is_square date.day && is_square date.month && is_square date.year

def next_birthdate (birthdate : Date) (today : Date) : Date :=
  let same_year := { birthdate with year := today.year }
  if today.month < birthdate.month ∨
     (today.month = birthdate.month ∧ today.day < birthdate.day) then
    same_year
  else
    { same_year with year := today.year + 1 }

def year_is_in_last_millenium (date : Date) : Bool :=
  1001 ≤ date.year && date.year ≤ 2000

def is_last_date_in_container (date : Date) (dates : List Date) (c : Date → Date → Bool) : Bool :=
  (dates.contains date) && dates.all (λ x => c x date || x == date)

def month_to_num_days : Nat → Nat
  | 1  => 31 | 2  => 28 | 3  => 31 | 4  => 30
  | 5  => 31 | 6  => 30 | 7  => 31 | 8  => 31
  | 9  => 30 | 10 => 31 | 11 => 30 | 12 => 31
  | _  => 0

def square_days (month : Nat) : List Nat :=
  List.range' 1 (month_to_num_days month) |>.filter is_square

def square_months : List Nat :=
  List.range' 1 13 |>.filter is_square

def square_month_day_pairs : List (Nat × Nat) :=
  square_months >>= fun month =>
    let num_days := month_to_num_days month
    (square_days month).filter (· ≤ num_days)
      |>.map (λ day => (month, day))

-- Gets dates inclusive between <date_left>, <date_right>
def get_dates_in_range (date_left : Date) (date_right : Date) : List Date :=
  let year_count := date_right.year - date_left.year + 1
  let years := List.filter is_square (List.range' date_left.year year_count)

  square_month_day_pairs >>= fun (month, day) =>
    years |> List.map (fun y => { month := month, day := day, year := y : Date })

def get_square_dates_in_range (date_left : Date) (date_right : Date) : List Date :=
  List.filter (λ date => is_square_date date) (get_dates_in_range date_left date_right)

def date_le_b (x y : Date) : Bool :=
  x.year < y.year || (x.year == y.year && (x.month < y.month || (x.month == y.month && x.day <= y.day)))

/-
Main Theorems & Definitions

Formally proves the puzzle with one caveat:
This lean proof does not consider leap year.
This is not a problem since 2/29/<year> is not
a square or cubic date, but regardless, makes
it slightly incomplete.
-/

-- oldest documented human was at most 130 years old
def max_human_lifespan : Nat := 130
def today : Date := ⟨ 6, 1, 2025 ⟩
def my_birthdate : Date := ⟨ 9, 25, 1972 ⟩
def mothers_birthdate : Date := ⟨ 8, 1, 1936 ⟩

def is_my_birthdate (my_birthdate : Date) (today : Date) : Bool :=
  let my_next_birthdate := next_birthdate my_birthdate today
  let years_left_from_today := max_human_lifespan - (today.year - my_birthdate.year)
  let my_life_upper_bound := { my_birthdate with year := today.year + years_left_from_today }
  let next_square_dates_in_lifespan := get_square_dates_in_range today my_life_upper_bound

  (year_is_in_last_millenium my_birthdate) &&
  is_last_date_in_container my_next_birthdate next_square_dates_in_lifespan date_le_b &&
  today.year == my_birthdate.year + (sqrt my_next_birthdate.year + sqrt my_birthdate.month + sqrt my_birthdate.day)

def is_mothers_birthdate (mothers_birthdate : Date) : Bool :=
  (!is_square mothers_birthdate.month || (is_square_date {mothers_birthdate with month := 1}))
  && (!is_square_date mothers_birthdate)
  && (is_cubic mothers_birthdate.day)
  && (is_cubic mothers_birthdate.month)

theorem my_birthdate_is_9_25_1972 : is_my_birthdate my_birthdate today = true := by
  simp [is_my_birthdate, my_birthdate, today, next_birthdate]
  decide

theorem my_mothers_birthdate_is_8_1_1936 : is_mothers_birthdate mothers_birthdate = true := by
  simp [is_mothers_birthdate, mothers_birthdate]
  decide
